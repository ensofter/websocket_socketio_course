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
        print('присоединился новый пользователь')

    @sio.on('join')
    def join_now(sid, data):
        room = data['room']

        user_rooms = sio.rooms(sid)
        user_rooms.remove(sid)
        if len(user_rooms) > 0:
            print('YEs')
            sio.leave_room(sid, user_rooms[0])
            sio.enter_room(sid, room)
        else:
            sio.enter_room(sid, room)


        rooms_data = {}
        for user in users:
            user_rooms = sio.rooms(user)
            user_rooms.remove(user)
            for ur in user_rooms:
                if ur not in rooms_data:
                    rooms_data[ur] = [user]
                else:
                    rooms_data[ur] += [user]
        sio.emit('message', data=rooms_data)

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
