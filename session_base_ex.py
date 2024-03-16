import logger
import socketio
import eventlet


HOST = ('localhost', 12345)
log = logger.MyLogger()

def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        log.info(f'Клиент {sid} подключен')

    @sio.event
    def disconnect(sid):
        log.info(f'Клиент {sid} отключен')

    @sio.on('join')
    def join(sid, data):
        name = data.get('name')
        sio.save_session(sid=sid, session={'name': name})
        log.info(f'Пользователь {name} присоединился')

    @sio.on('message')
    def on_message(sid, data):
        text = data.get('text')
        name = sio.get_session(sid=sid).get('name')
        log.info(f'Пользователь {name} пишет в чат {text}')
        sio.emit('message', {'text': text, 'name': name})

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
