#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from forklift_server.msg import TopologyMapActionGoal
import subprocess, os
from time import sleep
from std_msgs.msg import Bool, Float64, String
import threading
# from include_py import creat_navigation_info
# from .creat_navigation_info import write
from creat_navigation_info import SaveNavigationInfo
from robot_control.msg import Navigation_server
import actionlib
from move_base_msgs.msg import MoveBaseAction
from show_gif import FullscreenGIF
# from process import Process 

btn_text = [['急診', '放射'], ['藥局', '結束']]
closing_order = ['laser', 'TopologyMap', 'navigation', 'CeilingSLAMwithZED2', 'PBVS', 'continuous', 'ZED', 'D435', 'driver', 'gui']  # 設定關閉順序

class MainWindow(QtWidgets.QWidget):
    def __init__(self, screen_size, srceen_dpi, project_path):
        super().__init__()
        # self.setWindowTitle("Robot Control Interface")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # 移除整個視窗的標題列與邊框
        self.screen = screen_size # 得到畫面可以顯示範圍
        self.dpi = srceen_dpi  # 得到畫面的dpi
        self.project_path = project_path
        # print("Screen width:", self.screen.width(), "Screen height:", self.screen.height())
        self.resize(self.screen.width(), int(self.screen.height()))
        self.car_msg_window = CarMessageWindow(self.screen, self.dpi, self.project_path)
        self.yesno_window = YesNoWindow(self.screen, self.project_path)
        self.gif_gui = FullscreenGIF(self, self.screen, self.dpi, self.project_path)
        self.Btn = BtnPush(project_path)
        self.btn = [[None] * 2 for _ in range(2)]
        self.inactivity_timer = QtCore.QTimer(self)
        self.inactivity_timer.setInterval(10000)
        self.menu_ui()

    def menu_ui(self):
        btn_function = {btn_text[0][0]:self.Btn.p1, btn_text[0][1]:self.Btn.p2, btn_text[1][0]:self.Btn.p3, btn_text[1][1]:self.Btn.close}
        
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(0) # 設定間距為 0
        grid.setContentsMargins(0, 0, 0, 0) # 移除內邊距

        button_size_width, button_size_height = int(self.width()//2), int(self.height()//2) # 設定按鈕大小
        
        for i in range(len(btn_text)):
            for j in range(len(btn_text[i])):
                self.btn[i][j] = QtWidgets.QPushButton()
                self.btn[i][j].setText(btn_text[i][j])
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 364*self.dpi//188))
                self.btn[i][j].setStyleSheet('''
                                             QPushButton{
                                             border : 3px solid gray;
                                             background-color : white;
                                             }''')
                self.btn[i][j].setFixedSize(button_size_width, button_size_height)
                # self.btn[i][j].setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
                self.btn[i][j].pressed.connect(lambda x=i, y=j: self.Btn.btn_pressed(x, y))  # 當按鈕"按下"時，所要執行的函式
                self.btn[i][j].released.connect(btn_function[btn_text[i][j]]) # 當按鈕"放開"時，所要執行的函式
                grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

        self.setLayout(grid)
        self.inactivity_timer.timeout.connect(self.screensaver)
        self.installEventFilter(self)

    def screensaver(self):  # 當一段時間 UI 都沒有變化時，就顯示螢幕保護程式
        self.removeEventFilter(self) # 解除主視窗的事件檢測
        self.inactivity_timer.stop()
        self.gif_gui.showGIF()

    def eventFilter(self, source, event):  # 當 UI 有發生變化，就重新計時
        if event.type() == QtCore.QEvent.Paint:
            self.inactivity_timer.start()
        return super().eventFilter(source, event)
    
    def resume_timer(self):
        self.installEventFilter(self) # 安裝主視窗的事件檢測
        self.inactivity_timer.start()

class CarMessageWindow(QtWidgets.QDialog):
    def __init__(self, screen_size, srceen_dpi, project_path):
        super().__init__()
        self.setWindowTitle("車子低電量警告")
        self.screen = screen_size
        self.dpi = srceen_dpi
        self.low_power_image_path = project_path + "/icon/low-battery.png"
        self.apply_image_path = project_path + "/icon/check.png"
        self.car_power = 0
        self.car_enable = True
        self.n = 0
        window_width, window_height = int(self.screen.width()*0.8), int(self.screen.height()*0.9)
        self.resize(window_width, window_height)
        self.move(((self.screen.width() - window_width) // 2), ((self.screen.height() - window_height) // 2))
        rospy.Subscriber("/car_voltage", Float64, self.get_car_power, queue_size=1)
        self.ui()

    def ui(self):
        msg_layout = QtWidgets.QVBoxLayout(self)

        # 顯示沒電圖示的label
        lab_icon = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self.low_power_image_path) # 載入沒電的圖片
        pixmap_size = int((750*self.dpi//188))
        scaled_pixmap = pixmap.scaled(int(pixmap_size*1.76552), pixmap_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)  # 調整圖片尺寸，其中1.76552是圖片長與寬的比例
        lab_icon.setPixmap(scaled_pixmap)
        lab_icon.setAlignment(QtCore.Qt.AlignCenter)
        msg_layout.addWidget(lab_icon)

        # 按鈕
        self.mbtn = QtWidgets.QPushButton()
        self.mbtn.setText("OK")
        self.mbtn.setFont(QtGui.QFont('Times New Roman', int(200*self.dpi//188)))
        check_icon = QtGui.QIcon(QtGui.QPixmap(self.apply_image_path))
        self.mbtn.setIcon(check_icon) 
        self.mbtn.setIconSize(QtCore.QSize(self.mbtn.size()*0.7*self.dpi/188))
        self.mbtn.setStyleSheet("QPushButton{border : 2px solid black;background-color : white;}")
        self.mbtn.pressed.connect(self.btn_pressed)  # 當按鈕"按下"時，所要執行的函式
        self.mbtn.released.connect(self.btn) # 當按鈕"放開"時，所要執行的函式
        # self.mbtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        msg_layout.addWidget(self.mbtn)

    def get_car_power(self, msg):
        self.car_power = msg.data
        if self.car_power < 23 and self.car_enable:
            self.n += 1
            if self.n > 2 :     # 當資料連續三筆都小於低電壓的閥值時，則判定車子沒電
                self.exec_()
                self.car_enable = False
        elif self.car_enable and self.n > 0 : self.n = 0

    def btn_pressed(self):        # 當按鈕按下時，會將按鈕背景顏色改成黃色
        self.mbtn.setStyleSheet("QPushButton{border : 2px solid black;background-color : yellow;}")
        self.mbtn.repaint()
        sleep(0.1)

    def btn(self):
        self.mbtn.setStyleSheet("QPushButton{border : 2px solid black;background-color : white;}")
        window.installEventFilter(window) # 安裝主視窗的事件檢測
        self.close()

    def showEvent(self, event):
        window.removeEventFilter(window) # 解除主視窗的事件檢測
        window.inactivity_timer.stop()
        super().showEvent(event)

class YesNoWindow(QtWidgets.QDialog):
    def __init__(self, screen_size, project_path):
        super().__init__()
        self.setWindowTitle("確認是否執行動作")
        self.screen = screen_size # 得到畫面可以顯示範圍
        self.apply_image_path = project_path + "/icon/check.png"    # 打勾圖示
        self.cancel_image_path = project_path + "/icon/delete.png"  # 打叉圖示
        self.resize(int(self.screen.width()*0.9), int(self.screen.height()*0.9))
        self.move(int((self.screen.width() - self.screen.width()*0.9) // 2), int((self.screen.height() - self.screen.height()*0.9) // 2))
        self.inactivity_timer = QtCore.QTimer(self)
        self.inactivity_timer.setInterval(10000)
        self.ui()

    def ui(self):
        button_size_height = int(self.height()*0.93) # 按鈕的高度
        button_size_width = int(self.width()*0.95//2)

        self.msg_layout = QtWidgets.QHBoxLayout(self)
        
        # Yes按鈕
        self.Ybtn = QtWidgets.QPushButton()
        yes_icon = QtGui.QIcon(QtGui.QPixmap(self.apply_image_path))
        self.Ybtn.setIcon(yes_icon)
        self.Ybtn.setFixedSize(button_size_width, button_size_height)
        self.Ybtn.setStyleSheet("QPushButton{border : 3px solid gray;background-color : white;}")
        self.Ybtn.setIconSize(QtCore.QSize(self.Ybtn.size()*0.9))
        self.Ybtn.pressed.connect(lambda x="Yes": self.btn_pressed(x))  # 當按鈕"按下"時，所要執行的函式
        self.Ybtn.released.connect(self.accept) # 當按鈕"放開"時，所要執行的函式，其中函式為QDialog提供的方法
        # self.Ybtn.clicked.connect(self.accept)  # QDialog提供的方法
        # self.Ybtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        self.msg_layout.addWidget(self.Ybtn)

        # No按鈕
        self.Nbtn = QtWidgets.QPushButton()
        no_icon = QtGui.QIcon(QtGui.QPixmap(self.cancel_image_path))
        self.Nbtn.setIcon(no_icon)
        self.Nbtn.setFixedSize(button_size_width, button_size_height)
        self.Nbtn.setStyleSheet("QPushButton{border : 3px solid gray;background-color : white;}")
        self.Nbtn.setIconSize(self.Nbtn.size()*0.9)
        self.Nbtn.pressed.connect(lambda x="No": self.btn_pressed(x))  # 當按鈕"按下"時，所要執行的函式
        self.Nbtn.released.connect(self.reject) # 當lightgray按鈕"放開"時，所要執行的函式，其中函式為QDialog提供的方法
        # self.Nbtn.clicked.connect(self.reject)  # QDialog提供的方法
        # self.Nbtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        self.msg_layout.addWidget(self.Nbtn)

        self.inactivity_timer.timeout.connect(self.reject) # 當一段時間都沒有去點選後，就關閉Yes/No視窗

    def btn_pressed(self, x):        # 當按鈕按下時，會根據回傳的x內容，將所對應的按鈕背景顏色改成黃色
        btn = (self.Ybtn if x == "Yes" else self.Nbtn)
        btn.setStyleSheet("QPushButton{border : 3px solid gray;background-color : yellow;}")
        btn.repaint()
        sleep(0.1)

    def accept(self):
        """覆寫 accept 方法"""
        self.Ybtn.setStyleSheet("QPushButton{border : 3px solid gray;background-color : white;}")
        self.inactivity_timer.stop()
        window.installEventFilter(window) # 安裝主視窗的事件檢測
        super().accept()  # 調用父類的 accept，關閉對話框

    def reject(self):
        """覆寫 reject 方法"""
        self.Nbtn.setStyleSheet("QPushButton{border : 3px solid gray;background-color : white;}")
        self.inactivity_timer.stop()
        window.installEventFilter(window) # 安裝主視窗的事件檢測
        super().reject()  # 調用父類的 reject，關閉對話框

    def showEvent(self, event):
        window.removeEventFilter(window) # 解除主視窗的事件檢測
        window.inactivity_timer.stop()
        super().showEvent(event)
        self.inactivity_timer.start()

class BtnPush():
    def __init__(self, project_path):
        self.navigation_goal = rospy.get_param("/TopologyMap_server/start_node", "P1")
        # self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)
        self.pub = rospy.Publisher("/GUI_NavigationMsg", Navigation_server, queue_size=1, latch=True)
        rospy.Subscriber("/NavigationGoalInfo", String, self.echo_navigation_goal, queue_size=1)
        self.navigation_state_pub = rospy.Publisher('/NavigationState', Bool, queue_size=1, latch=True)
        self.navigation_ctrl = Navigation_server()
        self.navigation_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.script_path = project_path + "/Script/restart_script_stage_1.sh"


    def btn_pressed(self, x, y):        # 當按鈕按下時，會根據回傳的x, y值，將所對應的按鈕背景顏色改成黃色
        # print(f"x:{x} y:{y}")
        window.btn[x][y].setStyleSheet("QPushButton{border : 3px solid gray;background-color : yellow}")
        window.btn[x][y].repaint()
        sleep(0.1)

    def p1(self):   # 急診
        window.btn[0][0].setStyleSheet("QPushButton{border : 3px solid gray;background-color : white}")
        # window.car_msg_window.exec_()
        if(window.car_msg_window.car_enable):
            ret = window.yesno_window.exec_()
            if ret == QtWidgets.QDialog.Rejected : return
            self.navigation_ctrl.mode = ['TopologyMap']
            self.navigation_ctrl.command = ['P11']
            # print(self.navigation_ctrl)
            self.pub.publish(self.navigation_ctrl)
            # print("急診")
        else :
            window.car_msg_window.exec_()
    
    def p2(self):   # 放射
        window.btn[0][1].setStyleSheet("QPushButton{border : 3px solid gray;background-color : white}")
        if(window.car_msg_window.car_enable):
            ret = window.yesno_window.exec_()
            if ret == QtWidgets.QDialog.Rejected : return
            # self.navigation_ctrl.mode = ['TopologyMap', 'PBVS']
            # self.navigation_ctrl.command = ['P6', 'parking_bodycamera']
            # print(self.navigation_ctrl)
            # self.pub.publish(self.navigation_ctrl)
            print("放射")
        else :
            window.car_msg_window.exec_()

    def p3(self):   # 藥局
        window.btn[1][0].setStyleSheet("QPushButton{border : 3px solid gray;background-color : white}")
        if(window.car_msg_window.car_enable):
            ret = window.yesno_window.exec_()
            # print('Yes' if ret == QtWidgets.QDialog.Accepted else "N0")
            if ret == QtWidgets.QDialog.Rejected : return
            self.navigation_ctrl.mode = ['TopologyMap', 'PBVS']
            self.navigation_ctrl.command = ['P6', 'parking_bodycamera']
            # self.navigation_ctrl.mode = ['TopologyMap']
            # self.navigation_ctrl.command = ['P6']
            # print(self.navigation_ctrl)
            self.pub.publish(self.navigation_ctrl)
            # print("藥局")
        else :
            window.car_msg_window.exec_()

    def close(self):
        window.btn[1][1].setStyleSheet("QPushButton{border : 3px solid gray;background-color : white}")
        ret = window.yesno_window.exec_()
        if ret == QtWidgets.QDialog.Rejected : return
        else : SaveNavigationInfo.write()
        # sleep(1)
        param = '-15'
        enable = False
        while True:
            process = Process.find_process()
            if len(process) <= 1 and enable: break
            # elif enable: param = '-9', print("Closing not completed yet!!!")
            Process.close(ros_process=process, kill_param=param)
            sleep(1)
            enable = True
        # print("close")
        subprocess.run(['dbus-send', '--type=method_call',
                        '--dest=org.gnome.ScreenSaver',
                        '/org/gnome/ScreenSaver',
                        'org.gnome.ScreenSaver.Lock'])
        subprocess.run(['systemctl', '--user', 'start', 'screen_lock.target'])

    # def pub_goal(self, goal_name=''):
    #     goal = TopologyMapActionGoal()
    #     goal.goal.goal = goal_name
    #     # print(goal)
    #     self.pub.publish(goal)

    def echo_navigation_goal(self, msg):
        self.navigation_goal = msg.data     # 接收Topology_map傳回來已經到達的導航點

class Process():
    def find_process():
        result = subprocess.run(['pgrep', '-fa', 'roslaunch|rosrun|roscore'], stdout=subprocess.PIPE)
        lines = result.stdout.decode().splitlines()

        process = {}
        for line in lines:
            parts = line.split()
            pid = parts[0]
            name = ''.join(parts[3:])
            process[name] = pid
            # print(f'name : {name}  PID : {pid}')
        
        return process

    def close(ros_process={}, kill_param='-15'):
        for i in closing_order:
            for command, command_pid in ros_process.items():
                if i in command:
                    if 'gui' in command: window.close()
                    print(f'name : {command}  PID : {command_pid}')
                    subprocess.run(['kill', kill_param, command_pid])
                    sleep(1)
                    break

class NavigationPlayMusic():
    def __init__(self, project_path):
        self.playerlist = QtMultimedia.QMediaPlaylist()
        self.player = QtMultimedia.QMediaPlayer()
        music_path = project_path + "/music/Free_Music.mp3"
        qurl = QtCore.QUrl.fromLocalFile(music_path)
        qmusic = QtMultimedia.QMediaContent(qurl)
        self.playerlist.addMedia(qmusic)
        self.playerlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playerlist)
        rospy.Subscriber('/MusicState', Bool, self.music_state, queue_size=1)

    def play_music(self):
        self.player.play()

    def stop_music(self):
        self.player.stop()

    def music_state(self, msg):
        if msg.data :
            self.play_music()

        else : self.stop_music()

if __name__ == "__main__":
    rospy.init_node('GUI_node')
    app = QtWidgets.QApplication(sys.argv)
    path = os.path.dirname(os.path.dirname(__file__)) # 專案路徑
    screen = app.primaryScreen().availableGeometry() # 得到畫面可以顯示範圍
    dpi = int(app.primaryScreen().physicalDotsPerInch())   # 得到畫面的dpi
    window = MainWindow(screen, dpi, path)
    player = NavigationPlayMusic(path)
    window.show()
    window.inactivity_timer.start()
    sys.exit(app.exec_())