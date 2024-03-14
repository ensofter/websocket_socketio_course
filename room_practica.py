import socketio
import eventlet


HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)


    @sio.event
    def connect(sid, environ):
        sio.enter_room(sid, 'lobby')
        print(f'Пользователь {sid} добавлен в команту lobby')
        sio.emit('update', data={'message': 'user_joined'}, skip_sid=sid)

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
