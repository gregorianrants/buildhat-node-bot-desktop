from build_hat_node_bot_shared.network_py.Subscriber import Subscriber
import zmq
import math

context = zmq.Context()

class Json_Subscriber(Subscriber):
    def __init__(self, context, subscribe_to_topic, subscribe_to_node="any"):
        super().__init__(context, subscribe_to_topic, subscribe_to_node)

    def __next__(self):
        return self.socket.recv_json()




subscriber = Json_Subscriber(context=context,subscribe_to_topic='odometry',subscribe_to_node='Robot')

class Odometry:
    def __init__(self):
        self.lastLeftPosition = None
        self.lastRightPosition = None
        self.x = 0
        self.y = 0
        self.theta = 0
        self.dl = None
        self.dr = None
        self.DISTANCE_BETWEEN_WHEELS = 176 #mm

    def updatePosition(self):
        dTheta = (self.dr - self.dl) / self.DISTANCE_BETWEEN_WHEELS 
        self.theta = self.theta + dTheta
        dc = (self.dl + self.dr)/2
        self.x = self.x -dc* math.sin(self.theta)
        self.y = self.y + dc *math.cos(self.theta)

    def updateLeft(self,pos):
        if not self.lastLeftPosition:
            self.lastLeftPosition = pos
            return
        self.dl = pos - self.lastLeftPosition
        self.lastLeftPosition = pos
        self.dr = 0
        self.updatePosition()

    def updateRight(self,pos):
        if not self.lastRightPosition:
            self.lastRightPosition = pos
            return
        self.dr = pos - self.lastRightPosition
        self.lastRightPosition = pos
        self.dl = 0
        self.updatePosition()




odometry = Odometry()

count=0
for msg in subscriber:
    #print(msg)
    if msg['side']=='right':
        odometry.updateRight(msg['pos'])
    else:
        odometry.updateLeft(msg['pos'])
    count = (count+1)%100
    if(count==0):
        print(f'x: {odometry.x/10}, y: {odometry.y/10}, theta: {(odometry.theta/ (2*math.pi))*360}',flush=True)
        