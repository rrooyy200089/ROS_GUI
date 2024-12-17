#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from forklift_server.msg import TopologyMapActionGoal
import subprocess, time, os
from std_msgs.msg import Bool, Float64
# from process import Process 

btn_text = [['急診室門口', '結束'], ['藥局', '重新啟動']]
closing_order = ['gui', 'laser', 'TopologyMap', 'navigation', 'SLAM', 'ZED', 'demo']  # 設定關閉順序

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.form_event = QtWidgets.QMainWindow()
        self.setWindowTitle("Robot Control Interface")
        self.screen = app.primaryScreen().availableGeometry() # 得到畫面可以顯示範圍
        print("Screen width:", self.screen.width(), "Screen height:", self.screen.height())
        self.resize(self.screen.width(), self.screen.height())
        # self.showMaximized()
        # self.resize(1500, 800)
        # self.setWindowState(self.WindowMaximized)
        self.btn = [[None] * 3 for _ in range(2)]
        rospy.Subscriber("/car_voltage", Float64, self.get_car_power, queue_size=1)
        self.car_enable = True

    def menu_ui(self):
        self.box = QtWidgets.QWidget(self)
        # self.box.setGeometry(0, 0, self.screen.width()-10, self.screen.height()-10)
        self.box.setGeometry(0, 0, self.width()-10, self.height()-45)
        # self.box.resize(self.width()-10, self.height()-70)
        print("Screen width:", self.box.width(), "Screen height:", self.box.height())
        self.grid = QtWidgets.QGridLayout(self.box)
        # self.mbox = QtWidgets.QMessageBox(self)
        # self.mbox.setInformativeText("請幫車子充電")
        # self.mbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "車子低電量警告", "車子電量過低", QtWidgets.QMessageBox.Ok)
        # self.mbox.setStyleSheet("QLabel {min-width: 300px; min-height: 300px;} QPushButton:hover{background-color: rgb(255, 93, 52);}")
        # self.mbox.setStyleSheet("QLabel {min-width: 300px; min-height: 300px;}")
        # self.mbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # self.mbox.setStyleSheet("QPushButton:hover{background-color: rgb(255, 93, 52);}")
        # self.mbox.setStyleSheet('''
        #                         QLabel{
        #                         font-size:23pt;
        #                         font-weight:bold;
        #                         text-align:center;
        #                         color:red;
        #                         min-height:8ex;
        #                         max-height:8ex;
        #                         }
        #                         QPushButton{
        #                         font-size:22pt;
        #                         min-height:3.2ex;
        #                         max-height:3.2ex;
        #                         min-width: 6.9ex;
        #                         max-width: 6.9ex;
        #                         icon-size: 33px;
        #                         }
        #                         ''')
        
        # self.mbox.setStyleSheet('''
        #                         QLabel{
        #                         font-size:33px;
        #                         font-weight:bold;
        #                         text-align:center;
        #                         color:red;
        #                         min-height:150px;
        #                         max-height:150px;
        #                         }
        #                         QPushButton{
        #                         font-size:33px;
        #                         min-height:60px;
        #                         max-height:60px;
        #                         min-width: 130px;
        #                         max-width: 130px;
        #                         icon-size: 33px;
        #                         }
        #                         ''')
        
        # self.mbox.setIcon(QtWidgets.QMessageBox.Warning)
        # self.mbox.setWindowTitle("車子低電量警告")
        # self.mbox.setText("車子電量過低(00.00V)\n請先充電")
        # self.mbox.show()

        # self.mbox.setBaseSize(QtCore.QSize(1000, 1000))
        # self.mbox.sizeHint
        # self.mbox.setFont(QtGui.QFont('標楷體', 28))

        row_num = len(btn_text)
        for i in range(len(btn_text)):
            col_num = len(btn_text[i])
            for j in range(len(btn_text[i])):
                self.btn[i][j] = QtWidgets.QPushButton(self)
                self.btn[i][j].setText(btn_text[i][j])
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 70))
                # self.btn[i][j].setStyleSheet('''
                #                              font-size:40px;
                #                              ''')
                self.btn[i][j].setFixedSize(int((self.box.width()-15)/col_num), int((self.box.height()-15)/row_num))
                self.btn[i][j].clicked.connect(btn_function[btn_text[i][j]])
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

    def get_car_power(self, msg):
        self.car_power = msg.data
        if self.car_power < 26 and self.car_enable:
            self.message_display()
            self.car_enable = False

    def message_display(self):
        # self.mbox.warning(self, "車子低電量警告", f"車子電量過低({msg.data}V)\n請先充電")
        mbox = QtWidgets.QMessageBox()
        mbox.setStyleSheet('''
                    QLabel{
                    font-size:33px;
                    font-weight:bold;
                    text-align:center;
                    color:red;
                    min-height:150px;
                    max-height:150px;
                    }
                    QPushButton{
                    font-size:33px;
                    min-height:60px;
                    max-height:60px;
                    min-width: 130px;
                    max-width: 130px;
                    icon-size: 33px;
                    }
                    ''')
        mbox.setIcon(QtWidgets.QMessageBox.Warning)
        mbox.setWindowTitle("車子低電量警告")
        mbox.setText(f"車子電量過低({self.car_power}V)\n請先充電")
        mbox.exec()

    # def show(self):
    #     self.show()

    # def closeEvent(self, self.form.event):
        # pass

class BtnPush():
    def __init__(self):
        self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)

    def p1(self):
        if(window.car_enable):
            self.pub_goal(goal_name='P11')
        else :
            window.message_display()
        # print("P1")
        # player.play_music()

    def p2(self):
        if(window.car_enable):
            self.pub_goal(goal_name='P6')
        else :
            window.message_display()
        # print("P2")
        # player.stop_music()

    # def p3(self):
    #     self.pub_goal(goal_name='P6')
    #     # print("P3")

    # def p4(self):
    #     # self.pub_goal(goal_name='P4')
    #     print("P4")

    def close(self):
        Procecss.close()
        print("close")

    def reset(self):
        # if os.path.exists(script_path):  # 判斷檔案是否存在
        #     Procecss.close()
        #     Procecss.restart()
        # else :
        #     print('No such file !!')
        print("reset")

    def pub_goal(self, goal_name=''):
        goal = TopologyMapActionGoal()
        goal.goal.goal = goal_name
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
            result = subprocess.run(script_path, shell=True, capture_output=True, text=True)
            
            # 判斷是否執行成功
            if result.returncode == 0:
                print("Command executed successfully.")
                print(f"Output:\n{result.stdout}")  # 輸出結果
            else:
                print("Command failed with return code:", result.returncode)
                print(f"Error message:\n{result.stderr}")   # 錯誤訊息
        except Exception as e:
            print("An error occurred while running the command:", e)
        pass

class NavigationPlayMusic():
    def __init__(self):
        self.playerlist = QtMultimedia.QMediaPlaylist()
        self.player = QtMultimedia.QMediaPlayer()
        qurl = QtCore.QUrl.fromLocalFile(music_path)
        qmusic = QtMultimedia.QMediaContent(qurl)
        self.playerlist.addMedia(qmusic)
        self.playerlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playerlist)
        self.navigation_state_sub = rospy.Subscriber('/NavigationState', Bool, self.navigation_state, queue_size=1)

    def play_music(self):
        self.player.play()

    def stop_music(self):
        self.player.stop()

    def navigation_state(self, msg):
        if msg.data :
            self.play_music()

        else : self.stop_music()

if __name__ == "__main__":
    rospy.init_node('GUI_node')
    app = QtWidgets.QApplication(sys.argv)
    # while not rospy.is_shutdown():
    window = MainWindow()
    Btn = BtnPush()
    btn_function = {btn_text[0][0]:Btn.p1, btn_text[1][0]:Btn.p2, btn_text[0][1]:Btn.close, btn_text[1][1]:Btn.reset}
    window.menu_ui()
    script_path = os.path.dirname(os.path.dirname(__file__)) + "/Script/restart_script.sh"
    music_path = os.path.dirname(os.path.dirname(__file__)) + "/music/Free_Music.mp3"
    player = NavigationPlayMusic()
    # print(script_path)
    window.show()
    sys.exit(app.exec_())
    # while app.exec_(): pass
    # rospy.signal_shutdown("GUI is shutdown")          
    # sys.exit()
