import uvicorn
import socketio
import logger
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from typing import Any, Dict


log = logger.MyLogger()

def main():
    app = FastAPI()
    sio = socketio.AsyncServer(
        async_mode='asgi',
        cors_allowed_origins='*'
    )
    socket_app = socketio.ASGIApp(sio, app)

    @sio.event
    async def connect(sid, environ):
        print('connect', sid)

    @sio.event
    async def disconnect(sid):
        print(f'Ушел один из нас {sid}')

    @app.get("/")
    async def get_index():
        await sio.emit("message", "hello everyone")

    @app.post('/')
    async def post_index(request: Dict[Any, Any]):
        data = request['message']
        await sio.emit('message', data)

    uvicorn.run(socket_app, host='localhost', port=12345)


if __name__ == '__main__':
    main()
