import logger
import eventlet
import socketio


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    log.info(f'Initialize new socketio Server {sio}')
    app = socketio.WSGIApp(sio)
    log.info(f'Inittialize new wsgi app {app}')

    @sio.event
    def connect(sid, environ):
        sio.emit('message', to=sid, data={'content': f'Welcome to the server'})

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
