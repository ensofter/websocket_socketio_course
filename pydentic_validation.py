from pydantic import BaseModel, EmailStr, ValidationError
import socketio
from loguru import logger
import eventlet



class User(BaseModel):
    pk: int = None
    name: str = None
    email: EmailStr = None

    @classmethod
    def init_user(cls, pk: int, name: str, email: str):
        return cls(pk=pk, name=name, email=email)


if __name__ == '__main__':
    user: User = User.init_user(pk=32, name='Алиса', email='alice@random.me')

    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        ...

    @sio.on('join')
    def join(sid, data):
        try:
            user = User.init_user(**data)
            sio.emit('user', to=sid, data=user.model_dump())
        except ValidationError as e:
            errors = e.json()
            sio.emit('errors', data=errors)

    eventlet.wsgi.server(eventlet.listen(('localhost', 12345)), app)