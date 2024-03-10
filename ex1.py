import eventlet
import socketio
import logger

def main():
    log = logger.MyLogger()

    log.info('Создаем экземпляр синхронного сервера Socket.IO')
    sio = socketio.Server()

    log.info('Создаем WSGI приложение и связываем его с Socket.IO')
    app = socketio.WSGIApp(sio)

    log.info('Обработчик события подключения')
    @sio.event
    def connect(sid, environ):
        print(f'Ето что-то environ: {environ}')
        print(f'Клиент {sid} подключен')

    log.info('Обработчик события отключения')
    @sio.event
    def disconnect(sid):
        print(f'Клиент {sid} отключен')

    log.info('Запускаем eventlet веб-сервер')
    HOST = ('localhost', 12345)
    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
