import re
import gc
import json
import logging
import typing
import pathlib
import dataclasses
import pydantic
from quart import current_app
from contextlib import redirect_stdout, redirect_stderr, contextmanager
from quart import Quart
from quart_schema import QuartSchema, validate_request, validate_response, RequestSchemaValidationError
from quart_schema import validation
from . import loader, envs, exceptions, utils
from .log import LogManager


@dataclasses.dataclass
class LogkitInfo:
    uri: str
    path: str
    namespace: typing.Optional[str] = "/logkit"
    events_append: typing.Optional[str] = "append"
    logs_level: typing.Optional[str] = "warning"


@dataclasses.dataclass
class FunctionContext:
    request_id: str
    user_id: str
    app_id: str
    node_id: str
    # 右面板参数
    params: typing.Optional[dict]
    # 输入桩参数
    args: dict


@dataclasses.dataclass
class FunctionParams:
    id: str
    file: str
    working_dir: typing.Optional[str]
    context: FunctionContext
    logkit: LogkitInfo
    function: typing.Optional[str] = "main"


@dataclasses.dataclass
class FunctionResponse:
    id: str
    success: bool
    error: typing.Optional[str] = None
    data: typing.Optional[dict] = None


@dataclasses.dataclass
class FunctionReleaseParams:
    app_id: str


@dataclasses.dataclass
class FunctionReleaseResponse:
    success: bool


def acquire_resource(user_id, app_id, node_id):
    envs.userId = user_id
    envs.appId = app_id
    envs.nodeId = node_id
    return user_id, app_id, node_id


def release_resource(ctx):
    envs.userId = None
    envs.appId = None
    envs.nodeId = None


@contextmanager
def node_context(*args, **kwargs):
    resource = acquire_resource(*args, **kwargs)
    try:
        yield resource
    finally:
        release_resource(resource)


def create_app(working_dir='.', log_file='', new_log=False):
    log_path = pathlib.Path(log_file).parent.parent
    app = Quart(__name__)
    QuartSchema(app)

    @app.post("/")
    @validate_request(FunctionParams)
    # @validate_response(FunctionResponse)
    async def function_invoke(data: FunctionParams):
        user_id = data.context.user_id
        app_id = data.context.app_id
        node_id = data.context.node_id
        if new_log:
            log_dir = log_path / f'{app_id}-{user_id}-{node_id}'
            log_dir.mkdir(parents=True, exist_ok=True)
            log_name = log_dir / f'app-{app_id}-{node_id}'
        else:
            log_dir = log_path / app_id
            log_dir.mkdir(parents=True, exist_ok=True)
            log_name = log_dir / node_id
        if utils.should_log_rollover(str(log_name)):
            utils.do_log_rollover(str(log_name))
        with open(log_name, 'a', encoding='utf8') as f:
            with redirect_stdout(f), redirect_stderr(f), node_context(user_id, app_id, node_id):
                function = None
                try:
                    logging.debug(f'event: {data.context.args}')
                    function = load(data, working_dir)
                    ret = await function.call_func(data.context.request_id, data.context.args, data.context.params)
                    logging.debug(f'response: {ret}')
                    out_data = {key: value for key, value in ret.items() if
                                re.match(r"out\d+", key) and value is not None}
                    resp = FunctionResponse(id=data.id, success=True, data=out_data)
                except Exception as e:
                    if function is not None:
                        function.context.log.exception(f'event error: {e}')
                    else:
                        logging.exception(f'event error: {e}')
                    resp = FunctionResponse(id=data.id, success=False, error=str(e))

        resp = await app.make_response(dataclasses.asdict(resp))
        resp.timeout = 2
        return resp

    @app.errorhandler(RequestSchemaValidationError)
    async def handle_request_validation_error(error):
        if isinstance(error.validation_error, TypeError):
            err = str(error.validation_error)
        else:
            err = error.validation_error.json()

        return {"errors": err}, 400

    @app.post("/function/release")
    @validate_request(FunctionReleaseParams)
    @validate_response(FunctionReleaseResponse)
    async def function_release(data: FunctionReleaseParams) -> FunctionReleaseResponse:
        app.add_background_task(background_garbage_collection, data.app_id)
        return FunctionReleaseResponse(success=True)

    @app.get("/health/liveness")
    async def liveness():
        resp = await app.make_response("OK")
        resp.timeout = 2
        return resp

    @app.get("/health/readiness")
    async def readiness():
        resp = await app.make_response("OK")
        resp.timeout = 2
        return resp

    return app


async def background_garbage_collection(app_id):
    del_nodes = []
    for node_id, node_function in module_imported.items():
        if node_function.context.app_id == app_id:
            del_nodes.append(node_id)

    for node_id in del_nodes:
        current_app.logger.info(f'node {node_id} release')
        del module_imported[node_id]

    LogManager.clear_logger(app_id)

    gc.collect()

module_imported = {}


def load(data: FunctionParams, default_dir):
    user_id = data.context.user_id
    app_id = data.context.app_id
    node_id = data.context.node_id
    working_dir = data.working_dir if data.working_dir else default_dir
    filename = data.file
    function = data.function

    node_function = module_imported.get(f'{user_id}_{app_id}_{node_id}')
    if not node_function:
        logging.info(f'node {node_id} import function {function} from {filename}')
        node_function = loader.NodeFunction(user_id, app_id, node_id, working_dir, filename, function)
        module_imported[f'{user_id}_{app_id}_{node_id}'] = node_function

    node_function.update_logkit(data.logkit)
    return node_function


async def handle_event(event_data, working_dir='.'):
    model_class = validation._to_pydantic_model(FunctionParams)
    try:
        json_data = json.loads(event_data)
        data = model_class(**json_data)
        data = typing.cast(FunctionParams, data)
    except (json.decoder.JSONDecodeError, TypeError, pydantic.ValidationError) as error:
        logging.exception(f'event error: {error}')
        raise exceptions.RequestSchemaValidationError(error)

    function = None
    try:
        logging.debug(f'event: {data.context.args}')
        function = load(data, working_dir)
        ret = await function.call_func(data.context.request_id, data.context.args, data.context.params)
        logging.debug(f'response: {ret}')
        out_data = {key: value for key, value in ret.items() if re.match(r"out\d+", key)}
        resp = FunctionResponse(id=data.id, success=True, data=out_data)
    except Exception as e:
        if function is not None:
            function.context.log.exception(f'event error: {e}')
        else:
            logging.exception(f'event error: {e}')
        resp = FunctionResponse(id=data.id, success=False, error=str(e))

    return resp
