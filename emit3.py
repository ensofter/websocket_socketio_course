import logger
import eventlet
import socketio

log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    log.info('create new socket io server')
    sio = socketio.Server()

    log.info('Create new wsgi app')
    app = socketio.WSGIApp(sio)

    log.info('create new list for active connections')
    active_connections = []

    log.info('Add handler for new connections')
    @sio.event
    def connect(sid, enviton):
        log.info('Add sid to lst')
        active_connections.append(sid)
        print('Client is connected')
        print(active_connections)

    log.info('Add new handler for disconnections')
    @sio.event
    def disconnect(sid):
        log.info('Remove sid from lst')
        active_connections.remove(sid)
        print('Client is dicsonnected')
        print(active_connections)

    log.info('StartUp webserver')
    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
