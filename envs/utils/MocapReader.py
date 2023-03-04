import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
import time

rospy.init_node('mocap_reader')

DF_MOCAP_TOPIC = '/vrpn_client_node/RigidBody1/pose'


class MocapReader:

    def __init__(self, mocap_topic:str=DF_MOCAP_TOPIC):
        self.mocap_topic = mocap_topic
        self.pose_subscriber = rospy.Subscriber(self.mocap_topic, PoseStamped, callback=lambda msg: self.pose_callback(msg))
        self._cur_pos = None

        while self._cur_pos is None:
            time.sleep(0.1)
        print("Received First Message from Topic")
        time.sleep(1)

    @property
    def cur_pos(self):
        return self._cur_pos
    
    def pose_callback(self, msg):
        self._cur_pos = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])