import zmq
import cv2
import numpy as np
import sys
print(sys.path)
from vision.flood import flood
# sys.path.append(
#     "/home/gregor/Projects/build-hat-node-bot-desktop",
# )



from build_hat_node_bot_shared.network_py.Subscriber import register,Subscriber
from build_hat_node_bot_shared.network_py.Publisher import registerPublisher,Publisher

context = zmq.Context()

subscriber = Subscriber(context=context,subscribe_to_topic='frame',subscribe_to_node='any')
publisher = Publisher(context,'tcp://192.168.178.47','floor_detector','floor_detector_features')

for msg in subscriber:
    sending_node,topic,recieved_bytes = msg
    np_array = np.frombuffer(recieved_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, 1)
    processedImage,left_closest,right_closest = flood(image)
    publisher.send_json({'left_closest':left_closest, 'right_closest': right_closest })
    cv2.imshow('image', processedImage)
    cv2.waitKey(1)

