import logger
import socketio
import eventlet


log = logger.MyLogger()

HOST = ('localhost', 12345)


def main():
    log.info('Создаем экземпляр синхронного сервера Socket.Io')
    sio = socketio.Server()

    log.info('Обертка app для использования сервера WSGI')
    app = socketio.WSGIApp(sio)

    log.info('Эхо обработчик для всех событий')
    @sio.on('*')
    def catch_all(event, sid, data):
        print('Получено событие:', event)
        print('Данные:', data)

    log.info('Запускаем сервер eventlet на порту 12345')
    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()

