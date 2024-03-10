import logger
import socketio
import eventlet


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    log.info('Создаем экземпляр сервера Socket.IO')
    sio = socketio.Server(corts_allowed_origins='*')

    log.info('Создаем WSGI приложение')
    app = socketio.WSGIApp(sio)

    log.info('Обработчик события соединения')
    @sio.on('connect')
    def connect(sid, environ):
        sio.emit('hello', to=sid, data={'message': 'Word up bich!'})
        print('connect', sid)

    log.info('Запускаем eventlet WSGI сервер')
    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()

