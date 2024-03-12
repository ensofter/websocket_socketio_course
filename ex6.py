import logger
import socketio
from fastapi import FastAPI
import uvicorn


HOST = ('localhost', 12345)
log = logger.MyLogger()


def main():
    log.info('Создаем экземпляр FastAPI приложения')
    app = FastAPI()

    log.info('Создаем экзмпляр SocketIO с поддержкой асинхронного режима')
    sio = socketio.AsyncServer(async_mode='asgi')

    log.info('Оборачиваем FastAPI в SocketIO ASGI приложение')
    socket_app = socketio.ASGIApp(sio, app)

    @sio.event
    async def connect(sid, environ):
        print(f'Пользователь {sid} подключился')

    @sio.event
    async def disconnect(sid):
        print(f'Пользователь {sid} отключился')

    @app.get('/')
    async def get_index():
        return "It Works!"

    uvicorn.run(socket_app, host='localhost', port=12345)

if __name__ == '__main__':
    main()
