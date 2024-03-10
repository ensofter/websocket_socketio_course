import logger
import eventlet
import socketio


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    log.info(f'Создали socket_io сервер {sio}')
    app = socketio.WSGIApp(sio)
    log.info(f'Создали WSGI приложение {app}')

    connections = []

    log.info('Написали обработчик события connect')
    @sio.event
    def connect(sid, environ):
        connections.append(sid)
        log.info(f'добавили sid в список {connections}')

    @sio.event
    def disconnect(sid):
        connections.remove(sid)
        log.info(f'удалили sid из списка {connections}')

    @sio.on('get_users_online')
    def get_users(sid, data):
        log.info(f'Получили ивент get_users_online {data}')
        sio.emit('users', to=sid, data={'online': f'{len(connections)}'})

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
