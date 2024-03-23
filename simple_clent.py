import socketio
from loguru import logger

logger.info('Создаем клиента сокета')
sio = socketio.SimpleClient()

logger.info('Подключаем клиента к серверу')
sio.connect('ws://localhost:12345')

event, data = sio.receive()
logger.info(f'Получили ответ {event}, {data}')

logger.info('Отправляем сообщение')
sio.emit('send_message', {'text': 'HELOL!!!'})
event, data = sio.receive()
logger.info(f'Получаем сообщение {event}, {data}')