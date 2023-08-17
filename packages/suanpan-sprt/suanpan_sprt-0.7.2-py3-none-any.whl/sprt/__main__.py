import logging
import sys
import signal
import asyncio
import click
import pathlib
from hypercorn.asyncio import serve
from hypercorn.config import Config
from logging.config import dictConfig
from . import server, envs, exceptions


@click.command()
@click.option('-h', '--host', default='localhost', envvar='RT_HOST', help='Runtime host')
@click.option('-p', '--port', default=19900, envvar='RT_PORT', help='Runtime port')
@click.option('-l', '--log-level', default='debug', envvar='RT_LOG_LEVEL', help='runtime logging level')
@click.option('-f', '--log-file', default='runtime.log', envvar='RT_LOG_FILE', help='runtime logging file')
@click.option('--new-log', default=False, envvar='RT_NEW_LOG', help='component with new log')
@click.option('-w', '--working-dir', default='.', envvar='RT_WORKING_DIR', help='working dir')
def main(host, port, log_level: str, log_file: str, new_log: bool, working_dir: str):
    pathlib.Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    if log_level.upper() in ('CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG'):
        dictConfig({
            'version': 1,
            'root': {
                'level': log_level.upper(),
                'handlers': ['console']
            },
            'handlers': {
                'console': {
                    'class': 'sprt.log.NodeStreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'std_out',
                    'stream': sys.stdout
                },
                'rotate_file': {
                    'level': 'DEBUG',
                    'formatter': 'std_out',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_file,
                    'encoding': 'utf8',
                    'maxBytes': 10000000,
                    'backupCount': 1,
                }
            },
            'formatters': {
                'std_out': {
                    'format': '%(asctime)s :: [%(levelname)-8s] %(message)s',
                    # 'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'loggers': {
                'sprt.server': {
                    'level': log_level.upper(),
                    'handlers': ['rotate_file'],
                    'propagate': False
                }
            },
        })

    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    app = server.create_app(working_dir, log_file, new_log)
    app.logger.info(f'use {log_file} {log_level} {new_log}')

    config = Config()
    config.bind = [f'{host}:{port}']
    if log_level.upper() == 'DEBUG':
        config.accesslog = log_file
    app.logger.info(f'python runtime running on {host}:{port}')
    asyncio.run(serve(app, config))


def receive_signal(signal_number, frame):
    print('receive_signal', signal_number)
    sys.exit(128 + signal_number)


@click.command()
@click.option('-e', '--event', default='', envvar='RT_EVENT', help='event message')
@click.option('-l', '--log-level', default='debug', envvar='RT_LOG_LEVEL', help='runtime logging level')
@click.option('-w', '--working-dir', default='.', envvar='RT_WORKING_DIR', help='working dir')
def run(event, log_level: str, working_dir: str):
    if log_level.upper() in ('CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG'):
        dictConfig({
            'version': 1,
            'root': {
                'level': log_level.upper(),
                'handlers': ['console']
            },
            'handlers': {
                'console': {
                    'class': 'sprt.log.NodeStreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'std_out',
                    'stream': sys.stdout
                }
            },
            'formatters': {
                'std_out': {
                    'format': '%(asctime)s :: [%(levelname)-8s] %(message)s',
                    # 'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'loggers': {
            },
        })

    try:
        resp = asyncio.run(server.handle_event(event, working_dir=working_dir))
        return resp
    except exceptions.RequestSchemaValidationError as e:
        print('invalid request:', e)
        exit(-1)


if __name__ == '__main__':
    main()
