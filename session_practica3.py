import logger
import eventlet
import socketio


HOST = ('localhost', 12345)
log = logger.MyLogger()


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    sids = []

    @sio.event
    def connect(sid, environ):
        sio.save_session(sid=sid, session={'owns_rooms': []})
        sids.append(sid)
        log.info(f'Зашел новый пользователь {sid}')
        log.info(f'Полный список пользователей {sids}')

    @sio.event
    def disconnect(sid):
        log.info('Пользователь покинул нас')
        sids.remove(sid)


    @sio.on('join')
    def join(sid, data):
        log.info('Обработчик входа в комнату')
        room = data.get('room')
        print('!!! Комната', room)
        is_it: bool = False
        for s in sids:
            sids_rooms = sio.rooms(s)
            print('!!!', sids_rooms)
            for r in sids_rooms:
                if r == room:
                    is_it = True
                    print('Такая комната уже есть')
        if not is_it:
            print('!!! никто еще такую комнату не зарегал')
            sio.enter_room(sid, room)
            log.info('Добавляем пользователю комнату в сессию')
            owns_rooms = sio.get_session(sid).get('owns_rooms')
            owns_rooms.append(room)
            sio.save_session(sid, session={'owns_rooms': owns_rooms})
            print('!!!', owns_rooms)
        else:
            sio.enter_room(sid, room)
            log.info('Это уже чья-то комната так что мы просто зайдем')

    @sio.on('profile')
    def profile(sid, data):
        sio.emit('profile', to=sid, data={'owns_rooms': sio.get_session(sid).get('owns_rooms')})

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
