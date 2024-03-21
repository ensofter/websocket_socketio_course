import eventlet
import pydantic
import socketio
from loguru import logger

HOST = ('localhost', 12345)


class Transfer(pydantic.BaseModel):
    amount: float
    ac_from: str = pydantic.Field(max_length=16)
    ac_to: str = pydantic.Field(pattern=r'[0-9]{16}')


def main():
    logger.info('Инициализировали wsgi приложение socketio')
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.on('create_transfer')
    def c_transfer(sid, data):
        logger.info('Запуск обработчика события create_transfer')
        try:
            transfer = Transfer(**data)
            logger.info(f'Получено событие на создание трансфера {transfer}')
            sio.emit('transfer', data=transfer.model_dump())
        except pydantic.ValidationError as e:
            logger.info(f'Возникла ошибка {e}')
            sio.emit('errors', data=e.json())

    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
