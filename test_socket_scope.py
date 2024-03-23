import pytest
import socketio


@pytest.fixture(scope='module')
def sio():
    socket_object = socketio.SimpleClient()
    client = socket_object.connect('ws://localhost:12345')
    socket_object.receive()
    return socket_object


@pytest.fixture(scope='module')
def sio_2():
    socket_object = socketio.SimpleClient()
    client = socket_object.connect('ws://localhost:12345')
    socket_object.receive()
    return socket_object


def test_chat(sio, sio_2):
    sio.emit('send_message', {'text': 'helol'})
    event, data = sio_2.receive()
    assert event == 'message'
    assert data == {'text': 'helol'}
