import socketio
import eventlet
from loguru import logger

HOST = ('localhost', 12345)
riddles = [
    {"text": "Не лает, не кусает, в дом не пускает", "answer": "замок"},
    {"text": "Зимой и летом одним цветом", "answer": "ель"},
    {"text": "Висит груша, нельзя скушать", "answer": "лампочка"}
]


users = {}


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        logger.info(f'Присоединился новый пользователь {sid}')
        if sid not in users:
            users[sid] = {'index': 0, 'score': 0}

    @sio.on('next')
    def start_handler(sid, data):
        logger.info(f'Пользователь {sid} начал игру')
        logger.info(f'Отправляем первую загадку')
        index = users[sid]['index']
        if index < len(riddles):
            sio.emit('riddle', to=sid, data=riddles[index]['text'])
        else:
            sio.emit('end', to=sid, data={'text': 'игра окончена'})

    @sio.on('answer')
    def answer_handler(sid, data):
        logger.info(f'Пользователя {sid} прислал ответ')
        answer = data['answer'].lower()
        logger.info(f'Ответ пользователя {answer}')
        index = users[sid]['index']
        if answer == riddles[index]['answer']:
            sio.emit('result', to=sid, data={'riddle': riddles[index]['text'], 'is_correct': True, 'answer': riddles[index]['answer']})
            users[sid]['score'] += 1
        else:
            sio.emit('result', to=sid, data={'riddle': riddles[index]['text'], 'is_correct': False, 'answer': riddles[index]['answer']})
        users[sid]['index'] += 1
        sio.emit('score', to=sid, data={'value': users[sid]['score']})


    eventlet.wsgi.server(eventlet.listen(HOST), app)


if __name__ == '__main__':
    main()
