import logger
import eventlet
import socketio


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    log.info('Создаем новый сокет сервер')
    sio = socketio.Server()
    log.info('Создаем новое wsgi приложение')
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        log.info(f'Присоединился новый сид {sid}')
        sio.emit('message', data={'content': 'New sid was connected'})
        sio.emit('message', to=sid, data={'content': 'WordUp bich!'})
        sio.emit('message', skip_sid=sid, data={'content': 'this message not for everyone'})

    log.info('Запускаем вебсервер с сокетом')
    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
