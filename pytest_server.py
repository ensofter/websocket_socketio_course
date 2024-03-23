import eventlet
import socketio


HOST = ('localhost', 12345)
sio = socketio.Server()
app = socketio.WSGIApp(sio)


def main():
    @sio.event()
    def connect(sid, environ):
        print(f'Клиент {sid} подключился')
        sio.enter_room(sid, 'lobby')
        print(f'Клиент зашел в комнату lobby')
        sio.emit('message', to=sid, data={'text': 'wellcome to the hell'})

    @sio.event()
    def disconnect(sid):
        print(f'Клиент {sid} отключился')

    @sio.on('send_message')
    def send_message(sid, data):
        text = data['text']
        sio.emit('message', {'text': text}, room='lobby')

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
