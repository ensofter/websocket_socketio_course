import datetime
import eventlet
import socketio


HOST = ('localhost', 12345)

def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    sid_time = {}

    @sio.event
    def connect(sid, enviton):
        print(f'Клиент подключился {sid}')
        if sid not in sid_time:
            sid_time[sid] = {'start': datetime.datetime.now(), 'end': ''}

    @sio.event
    def disconnect(sid):
        sid_time[sid]['end'] = datetime.datetime.now()
        print('!!!', sid_time[sid]['end'])
        total_time = sid_time[sid]["end"] - sid_time[sid]["start"]
        print(f'Климент отключился {sid}, время сессии {str(total_time)}')

    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
