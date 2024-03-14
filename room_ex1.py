import logger
import socketio
import eventlet
import json

log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    log.info(f'Инициализировали вебсокет сервер {sio}')
    app = socketio.WSGIApp(sio)
    log.info(f'Инициализировали wsgi приложение {app}')

    @sio.event
    def connect(sid, environ):
        log.info(f'Присоединился пользователь {sid}')
        print(f'User connect {sid}')

    @sio.on('join')
    def join(sid, data):
        log.info('Обработчик для команды Join')
        room = data['room']
        sio.enter_room(sid, room)
        print(f'User {sid} has joined to the room {room}')

    @sio.on('message')
    def message(sid, data):
        log.info('Обработчик для команды message в команту')
        text = data['text']
        room = data['room']
        sio.emit('message', {'text': text}, room=room)
        print(f'Message from {sid} in room {room}: {text}')



    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
