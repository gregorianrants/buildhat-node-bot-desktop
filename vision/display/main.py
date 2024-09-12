import sys
import zmq
import cv2
import numpy as np


sys.path.append(
    "/home/gregor/Projects/build-hat-node-bot-desktop",
)

print(sys.path)

from build_hat_node_bot_shared.network_py.Subscriber import register

context = zmq.Context()
fullAddress = register(context)
print(fullAddress)

#  Socket to talk to server

socket = context.socket(zmq.SUB)


socket.connect(fullAddress)
socket.setsockopt(zmq.SUBSCRIBE, b'')
socket.setsockopt(zmq.CONFLATE, 1)


while True:
    received_bytes = socket.recv()
    np_array = np.frombuffer(received_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, 1)
    cv2.imshow('image', image)
    cv2.waitKey(1)
