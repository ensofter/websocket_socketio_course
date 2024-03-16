import eventlet
import socketio


HOST = ('localhost', 12345)


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)


    users = []

    @sio.event
    def connect(sid, environ):
        users.append(sid)
        sio.enter_room(sid, 'lobby')

    @sio.on('message')
    def get_message(sid, data):
        room = data['room']

        if room == 'lobby':
            sio.leave_room(sid, 'lobby')
            print('удалили пользователя из группы')
        else:
            sio.emit('message', 'GGGGG Hey Joe', room=room)

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
