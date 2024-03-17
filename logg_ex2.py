from loguru import logger
import socketio
import eventlet
import sys


loguru_format = "<green>{time}</green><level>{message}</level>"
logger.add(sys.stdout, colorize=True, level='INFO', format=loguru_format)
logger.add('logs.log', level="INFO")


HOST = ('localhost', 12345)


def main():
    sio = socketio.Server()
    logger.warning(f'Создали сервер сокетов {sio}')

    app = socketio.WSGIApp(sio)
    logger.warning(f'Создали wsgi приложение {app}')

    @sio.event
    def connect(sid, environ):
        logger.warning('Обработчик для всех законнектившихся пользователей')

    @sio.event
    def disconnect(sid):
        logger.warning('Обрабочик для всех отключившихся пользователей')

    @sio.event
    def echo(sid, data):
        logger.warning(f'Полученно сообщение от {sid}: {data}')
        sio.emit('reply', data, to=sid)
        logger.warning(f'Это ответ на сообщение отправлено клиенту {sid}')

    logger.warning(f'Запуск сервера на хосте и порту {HOST}')
    try:
        eventlet.wsgi.server(eventlet.listen(HOST), app)
    except KeyboardInterrupt:
        logger.warning('Пользователь нажал Ctr+C')
    except Exception as e:
        logger.warning(f'Произошло падение по причине {e}')

if __name__ == '__main__':
    main()
