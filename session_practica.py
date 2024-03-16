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
        sio.save_session(sid=sid, session={'message_sent': 0})
        log.info(f'Создали сессию чуваку и установили в нее значение')


    @sio.on('message')
    def message(sid, data):
        text=data.get('text')
        sio.emit('broadcast', data={'text': text})
        message_sent = sio.get_session(sid=sid).get('message_sent')
        message_sent += 1
        sio.save_session(sid=sid, session={'message_sent': message_sent})
        log.info(f'ОТПРВЛЕНО СООБЩЕНИЦ: {message_sent}')


    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
