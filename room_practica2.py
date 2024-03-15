import socketio
import eventlet
import logger


log = logger.MyLogger()
HOST = ('localhost', 12345)


def main():
    log.info('Инициализируем сокет сервер')
    sio = socketio.Server()
    log.info('Инициализируем wsgi приложение')
    app = socketio.WSGIApp(sio)

    users = []

    @sio.event
    def connect(sid, environ):
        log.info('Обработчик для всех подключившихся')
        sio.enter_room(sid, 'lobby')
        users.append(sid)

    @sio.on('join')
    def join_to_room(sid, data):
        log.info('Подключаем пользователя к комнате')
        room = data['room']
        sio.enter_room(sid, room)
        print('пользователь подключился к комнате')
        rooms_data = {}
        for user in users:
            sid_rooms = sio.rooms(user)
            for sid_r in sid_rooms:
                if sid_r != user:
                    if sid_r not in rooms_data:
                        rooms_data[sid_r] = [user]
                    else:
                        rooms_data[sid_r] += [user]
        for i in rooms_data:
            print(i)
        sio.emit('message', data=rooms_data)

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
