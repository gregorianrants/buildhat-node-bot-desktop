import zmq
import time


def register(context):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.178.47:3000")

    success = False

    while not success:
        socket.send_json(
            {"action": "register", "register_as": "subscriber", "topic": "camera"}
        )

        message = socket.recv_json()
        if message['result'] == 'success':
            success = True
            return message['data']['fullAddress']
        time.sleep(0.1)
        print('still in loop')
