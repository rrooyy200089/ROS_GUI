#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore
from forklift_server.msg import TopologyMapActionGoal

from rviz import bindings as rviz

btn_text = [['1', '2', '3'], ['4', '5', '6']]

class MainWindow():
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        # self.form_event = QtWidgets.QMainWindow()
        self.form.setWindowTitle("Robot Control Interface")
        self.form.resize(1500, 800)
        # self.form.showMaximized()
        self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)
        # self.frame = rviz.VisualizationFrame()      # 創建一個 RViz 的 VisualizationFrame
        # self.frame.initialize()     # 初始化 RViz
        self.btn = [[None] * 3 for _ in range(2)]

    def menu_ui(self, goal_list=[]):
        self.box = QtWidgets.QWidget(self.form)
        self.box.setGeometry(0, 0, self.form.width()-10, self.form.height()-10)
        self.grid = QtWidgets.QGridLayout(self.box)

        for i in range(len(btn_text)):
            row_num = len(btn_text)
            col_num = len(btn_text[i])
            for j in range(len(btn_text[i])):
                self.btn[i][j] = QtWidgets.QPushButton(self.form)
                self.btn[i][j].setText(btn_text[i][j])
                self.btn[i][j].setFixedSize(int((self.form.width()-10)/col_num), int((self.form.height()-10)/row_num))
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)
                self.btn[i][j].clicked.connect(Btn.btn_0_0())

        # self.box = QtWidgets.QComboBox(self.form)
        # self.box.addItems(goal_list)
        # self.box.setGeometry(1100, 400, 250, 50)
        # self.btn = QtWidgets.QPushButton(self.form)
        # self.btn.setText('發布導航點')
        # self.btn.setGeometry(1100, 500, 250, 50)
        # self.lab1 = QtWidgets.QLabel(self.form)
        # self.lab1.setGeometry(1100, 600, 250, 50)
        # self.btn.clicked.connect(self.pub_goal)
        # self.rviz_ui()

    def rviz_ui(self):
        # self.frame.setSplashPath( "" )
        self.frame.setMenuBar( None )
        # self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile(config, "/home/roy/project/gui_ws/src/robot_control/node/GUI_rviz.rviz")
        self.frame.load(config)

        layout = QtWidgets.QWidget(self.form)
        layout.setGeometry(10, 10, 1000, 780)

        rviz_layout = QtWidgets.QVBoxLayout(layout)
        rviz_layout.addWidget(self.frame)

    def pub_goal(self):
        goal_name = self.box.currentText()
        self.lab1.setText(f"Go to：{goal_name}")
        goal = TopologyMapActionGoal()
        goal.goal.goal = goal_name
        # print(goal)
        self.pub.publish(goal)

    def show(self):
        self.form.show()

    # def closeEvent(self, self.form.event):
        # pass

class BtnPush():
    def btn_0_0():
        pass

        

# class MyMainWindow():
#     def __init__(self):
#         self.app = QtWidgets.QApplication(sys.argv)
#         self.form = QtWidgets.QWidget()
#         self.form.setWindowTitle("test gui")
#         self.form.resize(1500, 800)

#     def menu(self, goal_list=[]):
#         self.box = QtWidgets.QComboBox(self.form)
#         self.box.addItems(goal_list)
#         self.box.setGeometry(1100, 400, 250, 50)
#         self.btn = QtWidgets.QPushButton(self.form)
#         self.btn.setText('發布導航點')
#         self.btn.setGeometry(1100, 500, 250, 50)
#         self.btn.clicked.connect(self.p)
#         self.lab1 = QtWidgets.QLabel(self.form)
#         self.lab1.setGeometry(1100, 600, 250, 50)

#     def p(self):
#         self.lab1.setText(f"Go to：{self.box.currentText()}")
#         # pub = rospy.Publisher("/jssjsjsj/yyyy", String, queue_size=10)
#         pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)
#         # client = actionlib.SimpleActionClient('TopologyMap_server', forklift_server.msg.TopologyMapAction)
#         # client.wait_for_server()
#         # goal = forklift_server.msg.TopologyMapActionGoal(goal=self.box.currentText())
#         goal = TopologyMapActionGoal()
#         goal.goal.goal = self.box.currentText()
#         print(goal)
#         pub.publish(goal)
#         # goal = MoveBaseActionGoal()
#         # goal.goal_id.

#     def show(self):
#         self.form.show()

class LaunchParam():
    def __init__(self):
        self.waypoints = rospy.get_param('TopologyMap_server/waypoints')

    def goal_list(self):
        return list(self.waypoints.keys())

if __name__ == "__main__":
    rospy.init_node('GUI_node')
    app = QtWidgets.QApplication(sys.argv)
    # if rospy.has_param('TopologyMap_server/waypoints'):
        # while not rospy.is_shutdown():
    # sub = LaunchParam()
    window = MainWindow()
    Btn = BtnPush()
    # print(sub.goal_list())
    # window.menu_ui(goal_list=sub.goal_list())
    window.menu_ui(goal_list=[])
    window.show()
    sys.exit(app.exec_())
    # while app.exec_(): pass
    # rospy.signal_shutdown("GUI is shutdown")          
    # sys.exit()
    # else :
    #     rospy.loginfo("找不到TopologyMap_server/waypoints")

