import eventlet
import socketio

HOST = ('localhost', 12345)

def main():
    statick_files = {'/': 'index.html'}
    sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
    app = socketio.WSGIApp(sio, static_files=statick_files)

    @sio.event
    def connect(sid, environ):
        print(f'Пользователь {sid} подключился')

    @sio.event
    def disconnect(sid):
        print(f'Пользователь {sid} отключился')

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
