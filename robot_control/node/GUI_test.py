#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from forklift_server.msg import TopologyMapActionGoal

btn_text = [['導航點1', '導航點2', '結束'], ['導航點3', '導航點4', '重新啟動']]

class MainWindow():
    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        # self.form_event = QtWidgets.QMainWindow()
        self.form.setWindowTitle("Robot Control Interface")
        self.form.resize(1500, 800)
        # self.form.showMaximized()
        self.btn = [[None] * 3 for _ in range(2)]

    def menu_ui(self, goal_list=[]):
        self.box = QtWidgets.QWidget(self.form)
        self.box.setGeometry(0, 0, self.form.width()-10, self.form.height()-10)
        self.grid = QtWidgets.QGridLayout(self.box)

        row_num = len(btn_text)
        for i in range(len(btn_text)):
            col_num = len(btn_text[i])
            for j in range(len(btn_text[i])):
                self.btn[i][j] = QtWidgets.QPushButton(self.form)
                self.btn[i][j].setText(btn_text[i][j])
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 40))
                # self.btn[i][j].setStyleSheet('''
                #                              font-size:40px;
                #                              ''')
                self.btn[i][j].setFixedSize(int((self.form.width()-10)/col_num), int((self.form.height()-10)/row_num))
                self.btn[i][j].clicked.connect(btn_function[btn_text[i][j]])
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

    def show(self):
        self.form.show()

    # def closeEvent(self, self.form.event):
        # pass

class BtnPush():
    def __init__(self):
        self.goal_name = ''
        self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)

    def p1(self):
        self.goal_name = 'P1'
        self.pub_goal()
        print("P1")

    def p2(self):
        self.goal_name = 'P2'
        self.pub_goal()
        print("P2")

    def p3(self):
        self.goal_name = 'P3'
        self.pub_goal()
        print("P3")

    def p4(self):
        self.goal_name = 'P4'
        self.pub_goal()
        print("P4")

    def close(self):
        print("close")

    def reset(self):
        print("reset")

    def pub_goal(self):
        goal = TopologyMapActionGoal()
        goal.goal.goal = self.goal_name
        print(goal)
        self.pub.publish(goal)


if __name__ == "__main__":
    rospy.init_node('GUI_node')
    app = QtWidgets.QApplication(sys.argv)
        # while not rospy.is_shutdown():
    window = MainWindow()
    Btn = BtnPush()
    btn_function = {'導航點1':Btn.p1, '導航點2':Btn.p2, '導航點3':Btn.p3, '導航點4':Btn.p4, '結束':Btn.close, '重新啟動':Btn.reset}
    window.menu_ui(goal_list=[])
    window.show()
    sys.exit(app.exec_())
    # while app.exec_(): pass
    # rospy.signal_shutdown("GUI is shutdown")          
    # sys.exit()
