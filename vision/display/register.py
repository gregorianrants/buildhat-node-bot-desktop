import zmq
import time


def register(context):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.178.47:3000")

    success = False

    while not success:
        socket.send_json(
            {"action": "register", 
             "register_as": "subscriber", 
             "subscribe_to_node": "camera", 
             "subscribe_to_topic": "frame"
             }
        )

        message = socket.recv_json()
        if message['result'] == 'success':
            success = True
            print('connected')
            return message['data']['fullAddress']
        time.sleep(0.1)
        #print('still in loop')
