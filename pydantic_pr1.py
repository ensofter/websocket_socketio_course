from typing import Optional

import eventlet
import socketio
from loguru import logger
from pydantic import BaseModel, ValidationError, Field

HOST = ('localhost', 12345)


class Product(BaseModel):
    title: str = Field(None, max_length=140)
    price: float = Field(gt=0)
    discount: float = 0


def main():
    logger.info('Инициализируем сервер вебсокета')
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        ...

    @sio.on('create_product')
    def create_product_handler(sid, data):
        logger.info('Хэндлер обработки события create_product')
        try:
            product = Product(**data)
            sio.emit('product', data=product.model_dump())
        except ValidationError as e:
            errors = e.json()
            sio.emit('errors', data=errors)

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
