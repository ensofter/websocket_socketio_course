import uvicorn
import logger
import socketio
from fastapi import FastAPI
from pydantic import BaseModel

class Sid(BaseModel):
    name: str

log = logger.MyLogger()


def main():
    log.info('Инициализируем приложение FastApi')
    app = FastAPI()
    log.info('Инициализируем асинхронный сокет сервер')
    sio = socketio.AsyncServer(async_mode='asgi')
    log.info('Поднимаем приложение socketio')
    socket_app = socketio.ASGIApp(sio, app)

    sid_lst = []
    @sio.event
    async def connect(sid, environ):
        log.info(f'Добавляем {sid} в список')
        sid_lst.append(sid)
        log.info(f'Добавили идентификатор в список {sid_lst}')

    @sio.event
    async def disconnect(sid):
        log.info(f'Удалили идентификатор {sid_lst} из списка')
        sid_lst.remove(sid)
        log.info(f'список такой {sid_lst}')

    @app.get('/')
    async def get_index():
        log.info('Отдаем список пользователю')
        return f"{sid_lst}"

    log.info('Поднимаем асинхронный веб сервер')
    uvicorn.run(socket_app, host='localhost', port=12345)

if __name__ == '__main__':
    main()
