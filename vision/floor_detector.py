import zmq
import cv2
import numpy as np
import sys
from flood import flood
import json


sys.path.append(
    "/home/gregor/Projects/build-hat-node-bot-desktop",
)

#print(sys.path)

from build_hat_node_bot_shared.registerSubscriber import register
from build_hat_node_bot_shared.registerPublisher import registerPublisher



context = zmq.Context()



fullAddress = register(context)
print(fullAddress)

publisherAddress =registerPublisher(context,'tcp://192.168.178.47','floor_detector','frame')
print(publisherAddress)



#  Socket to talk to server

socket = context.socket(zmq.SUB)
socket.connect(fullAddress)
socket.setsockopt(zmq.SUBSCRIBE, b'')
socket.setsockopt(zmq.CONFLATE, 1)

pubSocket = context.socket(zmq.PUB)
pubSocket.bind(publisherAddress)
print('publishing to:',publisherAddress)


while True:
    received_bytes = socket.recv()
    np_array = np.frombuffer(received_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, 1)
    processedImage,left_closest,right_closest = flood(image)
    pubSocket.send_string(json.dumps({'left_closest':left_closest, 'right_closest': right_closest }))
    cv2.imshow('image', processedImage)
    cv2.waitKey(1)
