import sys
import logging
from datetime import datetime, timezone
from urllib.parse import urljoin
from quart import current_app
from . import master, envs


class LogManager(object):
    _app_logger = {}
    _app_logkit_handler = {}

    def __init__(self):
        ...

    @classmethod
    def get_logger(cls, app_id: str):
        if app_id not in cls._app_logger:
            cls._app_logger[app_id] = cls._init_app_logger(app_id)
        return cls._app_logger[app_id]

    @classmethod
    def _init_app_logger(cls, app_id):
        logger = logging.getLogger(f'logkit_{app_id}')
        logger.propagate = False

        if len(logger.handlers) > 0:
            return logger

        formatter = logging.Formatter('%(asctime)s :: [%(levelname)-8s] %(message)s')
        sh = NodeStreamHandler()
        sh.setLevel('DEBUG')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        return logger

    @classmethod
    def update_logger(cls, app_id, logkit=None):
        logger = cls.get_logger(app_id)
        if not logger:
            return

        if logkit is None:
            logkit_handler = cls._app_logkit_handler.pop(app_id)
            if logkit_handler:
                current_app.logger.info('remove logkit handler: %s', logkit_handler.uri)
                logger.removeHandler(logkit_handler)
                logkit_handler.close()
        else:
            logkit_handler = cls._app_logkit_handler.get(app_id)
            if logkit_handler is None:
                current_app.logger.info('setup app %s logkit handler: %s', app_id, logkit.uri)
                lh = LogkitHandler(logkit.uri, logkit.namespace, logkit.path, logkit.events_append)
                lh.setLevel(logkit.logs_level.upper())
                logger.addHandler(lh)
                cls._app_logkit_handler[app_id] = lh

    @classmethod
    def clear_logger(cls, app_id):
        logkit_handler = cls._app_logkit_handler.pop(app_id)
        if logkit_handler:
            current_app.logger.info('close logkit handler: %s', logkit_handler.uri)
            logkit_handler.close()

        logger = cls._app_logger.pop(app_id)
        if logger:
            logger.handlers.clear()


class NodeStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream=stream)

    def get_stream(self):
        return sys.stdout

    def set_stream(self, _value):
        ...

    stream = property(get_stream, set_stream)


class LogkitHandler(logging.Handler):
    def __init__(self, uri, namespace, socketio_path, event):
        super().__init__()
        self.client = None
        self.uri = uri
        self.url = urljoin(uri, namespace)
        self.namespace = namespace
        self.socketio_path = socketio_path
        self.event = event

    def make_client(self):
        return master.sio(self.url, namespaces=self.namespace, socketio_path=self.socketio_path, wait_timeout=3)

    def send(self, msg):
        if not self.client:
            self.client = self.make_client()

        if self.client.connected:
            # socketio will reconnect automatically
            self.client.emit(self.event, data=msg, namespace=self.namespace)

    @staticmethod
    def make_pickle(record):
        app = envs.appId
        extra = {"node": envs.nodeId}
        data = (app,
                {
                    "level": record.levelname,
                    "title": record.getMessage(),
                    "data": extra,
                    "time": datetime.now(timezone.utc).isoformat(),
                })
        return data

    def emit(self, record):
        if not self.uri:
            return

        try:
            msg = self.make_pickle(record)
            self.send(msg)
        except Exception:  # noqa
            self.handleError(record)

    def close(self):
        """
        Closes the socket.
        """
        self.acquire()
        try:
            client = self.client
            if client:
                self.client = None
                client.reconnection_attempts = 1
                client.disconnect()
            super().close()
        finally:
            self.release()
