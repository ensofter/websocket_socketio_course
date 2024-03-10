import logger
import eventlet
import socketio


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    log.info(f'Create new socketio Server {sio}')
    app = socketio.WSGIApp(sio)
    log.info(f'Create new wsgi app {app}')

    active_users = []

    log.info('Create new handler for new connection')
    @sio.event
    def connect(sid, environ):
        active_users.append(sid)
        log.info(f'Add new connection to list {active_users}')
        sio.emit('message', to=sid, data={'content': f'Active connections: {active_users}'})
        log.info('Send message to all users except this about active connections')
        sio.emit('message', skip_sid=sid,  data={'content': f'{len(active_users)}'})

    log.info('Delete user from active users list')
    @sio.event
    def disconnect(sid):
        active_users.remove(sid)


    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
