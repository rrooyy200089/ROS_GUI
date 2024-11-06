#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from forklift_server.msg import TopologyMapActionGoal
import subprocess, time
# from process import Process 

btn_text = [['導航點1', '導航點2', '結束'], ['導航點3', '導航點4', '重新啟動']]
closing_order = ['gui', 'laser', 'TopologyMap', 'navigation', 'SLAM', 'ZED', 'demo']  # 設定關閉順序

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.form_event = QtWidgets.QMainWindow()
        self.setWindowTitle("Robot Control Interface")
        # self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.screen = app.primaryScreen().availableGeometry()
        print("Screen width:", self.screen.width(), "Screen height:", self.screen.height())
        self.resize(self.screen.width(), self.screen.height()) #高-70是因為要減掉畫面中頂部時間那一條的顯示，這樣才是視窗可以顯示的大小
        # self.showMaximized()
        # self.resize(1500, 800)
        # self.setWindowState(self.WindowMaximized)
        self.btn = [[None] * 3 for _ in range(2)]

    def menu_ui(self, goal_list=[]):
        self.box = QtWidgets.QWidget(self)
        # self.box.setGeometry(0, 0, self.screen.width()-10, self.screen.height()-10)
        self.box.setGeometry(0, 0, self.width()-10, self.height()-45)
        # self.box.resize(self.width()-10, self.height()-70)
        print("Screen width:", self.box.width(), "Screen height:", self.box.height())
        self.grid = QtWidgets.QGridLayout(self.box)

        row_num = len(btn_text)
        for i in range(len(btn_text)):
            col_num = len(btn_text[i])
            for j in range(len(btn_text[i])):
                self.btn[i][j] = QtWidgets.QPushButton(self)
                self.btn[i][j].setText(btn_text[i][j])
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 40))
                # self.btn[i][j].setStyleSheet('''
                #                              font-size:40px;
                #                              ''')
                self.btn[i][j].setFixedSize(int((self.box.width()-10)/col_num), int((self.box.height()-10)/row_num))
                self.btn[i][j].clicked.connect(btn_function[btn_text[i][j]])
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

    # def show(self):
    #     self.show()

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
        Procecss.close()
        print("close")

    def reset(self):
        # Procecss.close()
        # Procecss.restart()
        print("reset")

    def pub_goal(self):
        goal = TopologyMapActionGoal()
        goal.goal.goal = self.goal_name
        print(goal)
        self.pub.publish(goal)

class Procecss():
    def close():
        result = subprocess.run(['pgrep', '-fa', 'roslaunch|rosrun|roscore'], stdout=subprocess.PIPE)
        lines = result.stdout.decode().splitlines()

        ros_process = {}
        for line in lines:
            parts = line.split()
            pid = parts[0]
            name = ''.join(parts[3:])
            ros_process[name] = pid
            # print(f'name : {name}  PID : {pid}')

        for i in closing_order:
            for command, command_pid in ros_process.items():
                if i in command:
                    if 'gui' in command: window.close()
                    print(f'name : {command}  PID : {command_pid}')
                    subprocess.run(['kill', '-15', command_pid])
                    time.sleep(1)
                    break

    def restart():
        try:
            # 使用 subprocess.run 執行指令
            result = subprocess.run('~/project/gui_ws/src/robot_control/node/test.sh', shell=True, capture_output=True, text=True)
            
            # 判斷是否執行成功
            if result.returncode == 0:
                print("Command executed successfully.")
                print("Output:")
                print(result.stdout)  # 輸出結果
            else:
                print("Command failed with return code:", result.returncode)
                print("Error message:")
                print(result.stderr)  # 錯誤訊息
        except Exception as e:
            print("An error occurred while running the command:", e)
        pass


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
