#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import sys
from PyQt5 import QtWidgets
from move_base_msgs.msg import MoveBaseActionGoal
from forklift_server.msg import TopologyMapActionGoal
from std_msgs.msg import String
import actionlib

class MyMainWindow():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle("test gui")
        self.form.resize(1500, 800)

    def menu(self, goal_list=[]):
        self.box = QtWidgets.QComboBox(self.form)
        self.box.addItems(goal_list)
        self.box.setGeometry(1100, 400, 250, 50)
        self.btn = QtWidgets.QPushButton(self.form)
        self.btn.setText('發布導航點')
        self.btn.setGeometry(1100, 500, 250, 50)
        self.btn.clicked.connect(self.p)
        self.lab1 = QtWidgets.QLabel(self.form)
        self.lab1.setGeometry(1100, 600, 250, 50)

    def p(self):
        self.lab1.setText(f"Go to：{self.box.currentText()}")
        # pub = rospy.Publisher("/jssjsjsj/yyyy", String, queue_size=10)
        pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1)
        # client = actionlib.SimpleActionClient('TopologyMap_server', forklift_server.msg.TopologyMapAction)
        # client.wait_for_server()
        # goal = forklift_server.msg.TopologyMapActionGoal(goal=self.box.currentText())
        goal = TopologyMapActionGoal()
        goal.goal.goal = self.box.currentText()
        print(goal)
        pub.publish(goal)
        # goal = MoveBaseActionGoal()
        # goal.goal_id.

    def show(self):
        self.form.show()

class LaunchParam():
    def __init__(self):
        self.waypoints = rospy.get_param('TopologyMap_server/waypoints')

    def goal_list(self):
        return list(self.waypoints.keys())

if __name__ == "__main__":
    rospy.init_node('GUI_node')
    if rospy.has_param('TopologyMap_server/waypoints'):
        sub = LaunchParam()
        window = MyMainWindow()
        # print(sub.goal_list())
        window.menu(goal_list=sub.goal_list())
        window.show()
        sys.exit(window.app.exec_())
    else :
        rospy.loginfo("找不到TopologyMap_server/waypoints")

