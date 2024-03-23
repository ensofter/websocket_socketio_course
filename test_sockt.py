import socketio

SOCKET_SERVER = 'ws://localhost:12345'


def test_connection():
    sio = socketio.SimpleClient()
    sio.connect(SOCKET_SERVER)

    event, data = sio.receive()
    assert event == 'message'
    assert data == {'text': 'wellcome to the hell'}
