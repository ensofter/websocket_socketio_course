import logger
import socketio
import eventlet


log = logger.MyLogger()

HOST = ('localhost', 12345)

def main():
    log.info('Создаем словарь в котором будем хранить счетчики для каждого полключенного пользователя')
    count = {}

    log.info('Создаем сокет сервер')
    sio = socketio.Server()
    log.info('Создаем WSGI приложение')
    app = socketio.WSGIApp(sio)


    @sio.event
    def connect(sid, environ):
        count[sid] = 0
        log.info(f'При коннекте создаем в словаре пользователя {sid} -> count[sid]')

    @sio.on('increase')
    def add_one(sid, data):
        count[sid] += 1
        log.info('Добавляем единичку')

    @sio.on('decrease')
    def minus_one(sid, data):
        count[sid] -= 1
        log.info('Удаляем единичку')

    @sio.on('get_score')
    def get_count(sid, data):
        log.info('Поступило клиентсткое событие get_score')
        sio.emit('score', to=sid, data={'score': f'{count[sid]}'})
        log.info('Отправили серверное событие score')


    eventlet.wsgi.server(eventlet.listen(HOST), app)

if __name__ == '__main__':
    main()
