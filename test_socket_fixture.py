import pytest
import socketio

HOST = 'ws://localhost:12345'


@pytest.fixture(scope='module')
def sio():
    socket_object = socketio.SimpleClient()
    client = socket_object.connect(HOST)
    return socket_object


def test_connection(sio):
    event, data = sio.receive()
    assert event == 'message'
    assert data == {'text': 'wellcome to the hell'}


def test_message(sio):
    import time
    time.sleep(2)
    sio.emit('send_message', {'text': 'helol'})
    event, data = sio.receive()
    assert event == 'message'
    assert data == {'text': 'helol'}


