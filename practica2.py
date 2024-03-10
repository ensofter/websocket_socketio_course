import logger
import socketio
import eventlet


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    log.info('Создаем сервер сокетов')
    app = socketio.WSGIApp(sio)
    log.info('Создаем WSGI приложение')

    lost_queries = []
    connections = []

    @sio.event
    def connect(sid, environ):
        connections.append(sid)
        log.info(f'Добавили пользователя {sid}')

    @sio.event
    def disconnetct(sid):
        connections.remove(sid)
        log.info(f'Удалили пользователя {sid}')


    @sio.on('get_online_users')
    def get_users(sid, data):
        log.info(f'Поступило клиентское событие get_online_users')
        sio.emit('users', to=sid, data={'online': f'{len(connections)}'})
        log.info('Отправили серверное событие users')

    @sio.on('*')
    def all_events(event, sid, data):
        log.info('Сюда попадаем только если для этого ивента нет обработчика')
        log.info(f'Обработчика не событие {event} не существует')
        lost_queries.append(event)

    @sio.on('count_queries')
    def miss_queries(sid, data):
        log.info('Поступило клиентское событие count_queries')
        sio.emit('queries', to=sid, data={'lost': f'{lost_queries}'})

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
