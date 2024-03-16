import eventlet
import socketio
import random


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        print(f'Присоединился новый пользователь {sid}')
        rooms = ['red', 'green', 'blue']
        room = random.choice(rooms)
        print('!!!', room)
        sio.enter_room(sid, room)

    @sio.on('broadcast')
    def message(sid, data):
        text = data['text']
        u_rooms = sio.rooms(sid)
        u_rooms.remove(sid)
        sio.emit('message', 'hello', room=u_rooms[0], skip_sid=sid)


    eventlet.wsgi.server(eventlet.listen(('localhost', 12345)), app)

if __name__ == '__main__':
    main()
