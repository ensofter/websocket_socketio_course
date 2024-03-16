import logger
import eventlet
import socketio


HOST = ('localhost', 12345)
log = logger.MyLogger()


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        log.info(f'К нам приконнектился новый пользователь {sid}')

    @sio.event
    def disconnect(sid):
        log.info('От нас ушел лучший из лучших')

    @sio.on('join')
    def join(sid, data):
        name = data.get('name')
        surname = data.get('surname')
        id = data.get('id')
        sio.save_session(sid=sid, session={'name':name, 'surname': surname, 'id': id})

    @sio.on('get_profile')
    def get_profile(sid, data):
        profile_sid = data.get('sid')
        session = sio.get_session(sid=profile_sid)
        sio.emit('profile', data={'name': session['name'], 'surname': session['surname'], 'id': session['id']})


    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
