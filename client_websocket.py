import eventlet
import socketio
from loguru import logger

HOST = ('localhost', 12345)


def main():
    logger.info('Инициализируем веб-сокет')
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event()
    def connect(sid, environ):
        logger.info('Хэндлер обработки каждого присоединившегося пользователя')
        sio.enter_room(sid, 'lobby')
        logger.info('Пользователь зашел в комнату lobby')
        sio.emit('message', to=sid, data={'text': 'Доброе пожаловать в lobby'})

    @sio.event()
    def disconnect(sid):
        logger.info('Хэндлер обработки отключившихся пользователей')
        logger.info('Клиент отключился')

    @sio.on('send_message')
    def send_message(sid, data):
        text = data['text']
        sio.emit('message', data={'text': text}, room='lobby')

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
