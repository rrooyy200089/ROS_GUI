#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import actionlib
import forklift_server.msg
import apriltag_ros.msg
from robot_control.msg import Navigation_server
from std_msgs.msg import Bool

class Ctrl_Server():
    def __init__(self):
        rospy.Subscriber("/GUI_NavigationMsg", Navigation_server, self.Receive_message, queue_size=1)
        self.music_state_pub = rospy.Publisher('/MusicState', Bool, queue_size=1, latch=True)

    def PBVS_client(self, msg):
        client = actionlib.SimpleActionClient('PBVS_server', forklift_server.msg.PBVSAction)
        client.wait_for_server()
        command = forklift_server.msg.PBVSGoal(command=msg)
        # print("send ", command)
        client.send_goal(command)
        client.wait_for_result()
        return client.get_result()

    def TopologyMap_client(self, msg):
        client = actionlib.SimpleActionClient('TopologyMap_server', forklift_server.msg.TopologyMapAction)
        client.wait_for_server()
        goal = forklift_server.msg.TopologyMapGoal(goal=msg)
        # print("send ", goal)
        client.send_goal(goal)
        client.wait_for_result()
        return client.get_result()

    def AprilTag_client(self, msg):
        client = actionlib.SimpleActionClient('AprilTag_server', apriltag_ros.msg.AprilTagAction)
        client.wait_for_server()
        goal = apriltag_ros.msg.AprilTagGoal(goal=msg)
        # print("send ", goal)
        client.send_goal(goal)
        client.wait_for_result()
        return client.get_result()

    def Receive_message(self, msg):
        # print(msg)
        try :
            if(len(msg.mode) != len(msg.command)): raise
            self.music_state_pub.publish(True)
            for i in range(len(msg.mode)):
                # print(f'{msg.mode[i]} : {msg.command[i]}')
                if(msg.mode[i] == 'PBVS' and msg.command[i] == 'parking_bodycamera'):
                    result = self.AprilTag_client(True)
                    print("AprilTag_client result ", result)
                    result = self.PBVS_client(msg.command[i])
                    print("PBVS_client result ", result)
                    result = self.AprilTag_client(False)
                    print("AprilTag_client result ", result)

                elif(msg.mode[i] == 'TopologyMap'):
                    rospy.logwarn("send TopologyMap: %s", msg.command[i])
                    result = self.TopologyMap_client(msg.command[i])
                    print("TopologyMap result ", result)

                else :
                    raise

            self.music_state_pub.publish(False)
        
        except :
            rospy.logwarn("\nerror command:\n%s", msg)  


if __name__ == '__main__':
    rospy.init_node('ctrl_server')
    server = Ctrl_Server()
    rospy.spin()            