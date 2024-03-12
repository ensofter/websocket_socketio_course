import eventlet
from flask import Flask
import socketio
import logger


HOST = ('localhost', 12345)

log = logger.MyLogger()


def main():
    log.info('Создаем сокет сервер')
    sio = socketio.Server()

    log.info('Создаем экземпляр Flask приложения')
    flask_app = Flask(__name__)

    log.info('Создаем wsgi приложение')
    app = socketio.WSGIApp(sio, flask_app)

    @sio.event
    def connect(sid, environ):
        print(f'Пользователь {sid} подключился')

    @sio.event
    def disconnect(sid):
        print(f'Пользователь {sid} отключился')

    @flask_app.route('/')
    def page_index():
        return "It works"

    log.info('Запускаем веб сокет и фласк')
    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
