import socketio
import logger
import uvicorn
from fastapi import FastAPI


log = logger.MyLogger()

def main():
    log.info('Инициализируем FastApp приложение')
    app = FastAPI()
    log.info('Инициализируем серве socketio')
    sio = socketio.AsyncServer(async_mode='asgi')
    log.info('Инициализируем asgi приложение socketio')
    socket_app = socketio.ASGIApp(sio, app)

    log.info('Создаем счетчик пользователей')
    storage = {'user_counter': 0}

    @sio.event
    async def connect(sid, environ):
        log.info('Меняем счетчик пользователей')
        storage['user_counter'] += 1
        print(f'Пользователь {sid} подключился')

    @app.get('/')
    async def get_index():
        log.info('Отдаем счетчик пользователей')
        return f'user_counter = {storage["user_counter"]}'

    uvicorn.run(socket_app, host='localhost', port=12345)

if __name__ == '__main__':
    main()
