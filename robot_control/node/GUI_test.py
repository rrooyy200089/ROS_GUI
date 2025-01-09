#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from forklift_server.msg import TopologyMapActionGoal
import subprocess, time, os
from std_msgs.msg import Bool, Float64, String
import threading
# from include_py import creat_navigation_info
# from .creat_navigation_info import write
from creat_navigation_info import SaveNavigationInfo
# from process import Process 

btn_text = [['急診', '結束'], ['藥局', '重啟']]
closing_order = ['laser', 'TopologyMap', 'navigation', 'CeilingSLAMwithZED2', 'ZED', 'driver', 'gui']  # 設定關閉順序

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
        self.car_msg_window = CarMessageWindow()
        self.yesno_window = YesNoWindow()
        self.btn = [[None] * 3 for _ in range(2)]

    def menu_ui(self):
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
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 130)) #70
                self.btn[i][j].setStyleSheet('''
                                             QPushButton{
                                             border : 1px solid gray;
                                             }''')
                self.btn[i][j].setFixedSize(int((self.box.width()-15)/col_num), int((self.box.height()-15)/row_num))
                # self.btn[i][j].clicked.connect(btn_function[btn_text[i][j]])
                self.btn[i][j].setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
                self.btn[i][j].pressed.connect(lambda x=i, y=j: Btn.btn_pressed(x, y))  # 當按鈕"按下"時，所要執行的函式
                self.btn[i][j].released.connect(btn_function[btn_text[i][j]]) # 當按鈕"放開"時，所要執行的函式
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

    # def show(self):
    #     self.show()

    # def closeEvent(self, self.form.event):
        # pass

class CarMessageWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("車子低電量警告")
        self.screen = app.primaryScreen().availableGeometry() # 得到畫面可以顯示範圍
        # print("Screen width:", self.screen.width(), "Screen height:", self.screen.height())
        self.dpi = int(app.primaryScreen().physicalDotsPerInch())
        self.window_height = self.screen.height() - int(130*self.dpi//188)
        self.window_width = self.screen.width() - int(500*self.dpi//188)
        self.resize(self.window_width, self.window_height)
        self.move(((self.screen.width() - self.window_width) // 2), ((self.screen.height() - self.window_height) // 2))
        # self.resize(int(self.screen.width()*0.8), int(self.screen.height()*0.8))
        # self.move(int((self.screen.width() - self.screen.width()*0.8) // 2), int((self.screen.height() - self.screen.height()*0.8) // 2))
        # self.setGeometry((self.screen.width()/2)-(self.window_width/2), (self.screen.height()/2)-(self.window_height/2), self.window_width, self.window_height)
        rospy.Subscriber("/car_voltage", Float64, self.get_car_power, queue_size=1)
        self.car_power = 0
        self.car_enable = True
        self.image_path = project_path + "/icon/low-battery.png"
        self.ui()
        # print(f"svodnv  {app.primaryScreen().physicalDotsPerInch()}")

    def ui(self):
        self.mbox = QtWidgets.QWidget(self)
        self.mbox.setGeometry(0, 0, self.width()-(6*self.dpi//188), self.height()-(6*self.dpi//188))
        # # self.mbox.setGeometry(10, 10, 1400, 900)
        # print(f"vjskdbvu : {self.mbox.width()}")
        mgrid = QtWidgets.QGridLayout(self.mbox)

        # background_color = self.palette().color(self.backgroundRole())  # 得到視窗的背景顏色
        # color_name = background_color.name()  # 得到顏色的名稱

        lab_icon = QtWidgets.QLabel(self)
        # lab_icon_size = int(750*self.dpi//188)
        # lab_icon.resize(lab_icon_size, lab_icon_size)
        # lab_icon.setStyleSheet(f'''QLabel{{border : 2px solid {color_name};}}''')  # 將icon的邊框設成更背景顏色一樣，以便隱藏邊框
        # lab_icon.setStyleSheet(f'''QLabel{{border : 2px solid black;}}''')  # 將icon的邊框設成更背景顏色一樣，以便隱藏邊框
        pixmap = QtGui.QPixmap(self.image_path)
        pixmap_size = int(750*self.dpi//188)
        scaled_pixmap = pixmap.scaled(int(pixmap_size*1.76552), pixmap_size)  #1.76552是圖片長與寬的比例
        lab_icon.setPixmap(scaled_pixmap)
        lab_icon.setAlignment(QtCore.Qt.AlignCenter)
        mgrid.addWidget(lab_icon, 0, 0)

        self.mbtn = QtWidgets.QPushButton(self)
        self.mbtn.setText("OK")
        self.mbtn.setFont(QtGui.QFont('Times New Roman', int(200*self.dpi//188)))
        check_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        self.mbtn.setIcon(check_icon) 
        self.mbtn.setStyleSheet(f'''
                           QPushButton{{
                           min-height:{int(300*self.dpi//188)}px;
                           }}''')
        self.mbtn.setIconSize(self.mbtn.size() * 5)
        self.mbtn.pressed.connect(self.btn_pressed)  # 當按鈕"按下"時，所要執行的函式
        self.mbtn.released.connect(self.btn) # 當按鈕"放開"時，所要執行的函式
        # self.mbtn.clicked.connect(self.btn)
        self.mbtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        mgrid.addWidget(self.mbtn, 1, 0)

    def get_car_power(self, msg):
        self.car_power = msg.data
        if self.car_power < 23 and self.car_enable:
            # QtCore.QMetaObject.invokeMethod(self, "message_display", QtCore.Qt.QueuedConnection)
            # QtCore.QTimer.singleShot(0, self.message_display)
            # QtCore.QTimer.singleShot(0, lambda text = "沒電":self.message_display(message_text=text))
            self.exec_()
            self.car_enable = False

    def btn_pressed(self):        # 當按鈕按下時，會將按鈕背景顏色改成黃色
        self.mbtn.setStyleSheet(f"QPushButton{{background-color : yellow;min-height:{int(300*self.dpi//188)}px;}}")

    def btn(self):
        self.mbtn.setStyleSheet(f"QPushButton{{background-color : lightgray;min-height:{int(300*self.dpi//188)}px;}}")
        self.close()

class YesNoWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("確認是否執行動作")
        self.screen = app.primaryScreen().availableGeometry() # 得到畫面可以顯示範圍
        # print("Screen width:", self.screen.width(), "Screen height:", self.screen.height())
        self.dpi = int(app.primaryScreen().physicalDotsPerInch())
        # self.window_height = self.screen.height() - int(130*self.dpi//188)
        # self.window_width = self.screen.width() - int(500*self.dpi//188)
        self.resize(int(self.screen.width()*0.8), int(self.screen.height()*0.8))
        self.move(int((self.screen.width() - self.screen.width()*0.8) // 2), int((self.screen.height() - self.screen.height()*0.8) // 2))
        self.font_size = 160*self.dpi//188
        self.ui()

    def ui(self):
        self.box = QtWidgets.QWidget(self)
        self.box.setGeometry(0, 0, self.width()-(6*self.dpi//188), self.height()-(6*self.dpi//188))

        grid = QtWidgets.QGridLayout(self.box)
        
        self.Ybtn = QtWidgets.QPushButton(self)
        yes_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        self.Ybtn.setIcon(yes_icon)
        self.Ybtn.setStyleSheet(f'''
                           QPushButton{{
                           min-width:{int(((self.box.width()-25)//2)*self.dpi//188)}px;
                           min-height:{self.box.height()}px;
                           }}''')
        self.Ybtn.setIconSize(self.Ybtn.size() * 13)
        self.Ybtn.pressed.connect(lambda x="Yes": self.btn_pressed(x))  # 當按鈕"按下"時，所要執行的函式
        self.Ybtn.released.connect(self.accept) # 當按鈕"放開"時，所要執行的函式，其中函式為QDialog提供的方法
        # self.Ybtn.clicked.connect(self.accept)  # QDialog提供的方法
        self.Ybtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        grid.addWidget(self.Ybtn, 0, 0)

        self.Nbtn = QtWidgets.QPushButton(self)
        no_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton)
        self.Nbtn.setIcon(no_icon)
        self.Nbtn.setStyleSheet(f'''
                           QPushButton{{
                           min-width:{int(((self.box.width()-10)//2)*self.dpi//188)}px;
                           min-height:{self.box.height()}px;
                           }}''')
        self.Nbtn.setIconSize(self.Nbtn.size() * 13)
        self.Nbtn.pressed.connect(lambda x="No": self.btn_pressed(x))  # 當按鈕"按下"時，所要執行的函式
        self.Nbtn.released.connect(self.reject) # 當按鈕"放開"時，所要執行的函式，其中函式為QDialog提供的方法
        # self.Nbtn.clicked.connect(self.reject)  # QDialog提供的方法
        self.Nbtn.setFocusPolicy(QtCore.Qt.NoFocus)     # 不要讓按鈕聚焦
        grid.addWidget(self.Nbtn, 0, 1)

    def btn_pressed(self, x):        # 當按鈕按下時，會根據回傳的x內容，將所對應的按鈕背景顏色改成黃色
        (self.Ybtn if x == "Yes" else self.Nbtn).setStyleSheet(f"QPushButton{{background-color : yellow;min-width:{int(((self.box.width()-10)//2)*self.dpi//188)}px;min-height:{self.box.height()}px;}}")

    def accept(self):
        """覆寫 accept 方法"""
        self.Ybtn.setStyleSheet(f"QPushButton{{background-color : lightgray;min-width:{int(((self.box.width()-10)//2)*self.dpi//188)}px;min-height:{self.box.height()}px;}}")
        super().accept()  # 調用父類的 accept，關閉對話框

    def reject(self):
        """覆寫 reject 方法"""
        self.Nbtn.setStyleSheet(f"QPushButton{{background-color : lightgray;min-width:{int(((self.box.width()-10)//2)*self.dpi//188)}px;min-height:{self.box.height()}px;}}")
        super().reject()  # 調用父類的 reject，關閉對話框


class BtnPush():
    def __init__(self):
        self.navigation_goal=""
        self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)
        rospy.Subscriber("/NavigationGoalInfo", String, self.echo_navigation_goal, queue_size=1)

    def btn_pressed(self, x, y):        # 當按鈕按下時，會根據回傳的x, y值，將所對應的按鈕背景顏色改成黃色
        # print(f"x:{x} y:{y}")
        window.btn[x][y].setStyleSheet("background-color : yellow")

    def p1(self):
        window.btn[0][0].setStyleSheet("background-color : lightgray")
        # window.car_msg_window.exec_()
        if(window.car_msg_window.car_enable):
            ret = window.yesno_window.exec_()
            if ret == QtWidgets.QDialog.Rejected : return
            self.pub_goal(goal_name='P11')
        else :
            window.car_msg_window.exec_()

        # print("P1")
        # player.play_music()
    
    def p2(self):
        window.btn[1][0].setStyleSheet("background-color : lightgray")
        if(window.car_msg_window.car_enable):
            ret = window.yesno_window.exec_()
            # print('Yes' if ret == QtWidgets.QDialog.Accepted else "N0")
            if ret == QtWidgets.QDialog.Rejected : return
            self.pub_goal(goal_name='P6') #p6
        else :
            window.car_msg_window.exec_()
        # print("P2")
        # player.stop_music()

    # def p3(self):
    #     self.pub_goal(goal_name='P6')
    #     # print("P3")

    # def p4(self):
    #     # self.pub_goal(goal_name='P4')
    #     print("P4")

    def close(self, ask = True):
        window.btn[0][1].setStyleSheet("background-color : lightgray")
        if ask : 
            ret = window.yesno_window.exec_()
            if ret == QtWidgets.QDialog.Rejected : return
            else : SaveNavigationInfo.write()
        # time.sleep(1)
        param = '-15'
        enable = False
        while True:
            process = Process.find_process()
            if len(process) <= 1 and enable: break
            # elif enable: param = '-9', print("Closing not completed yet!!!")
            Process.close(ros_process=process, kill_param=param)
            time.sleep(1)
            enable = True
        print("close")

    def reset(self):
        window.btn[1][1].setStyleSheet("background-color : lightgray")
        ret = window.yesno_window.exec_()
        if ret == QtWidgets.QDialog.Rejected : return   
        SaveNavigationInfo.write(program_reset = True, goal_start = self.navigation_goal)
        # c = threading.Thread(target=self.close())
        # c.daemon = True
        # r = threading.Thread(target=Process.restart())
        # r.daemon = True
        if os.path.exists(script_path):  # 判斷檔案是否存在
            self.close(ask=False)
            # c.start()
            time.sleep(2)
            Process.restart()
            # c.start()
            # c.join()
            # time.sleep(2)
            # r = threading.Thread(target=Process.restart(), daemon=True)
            # r.start()
        else :
            print('No such file !!')
        # creat_navigation_info.write()
        print("reset")

    def pub_goal(self, goal_name=''):
        goal = TopologyMapActionGoal()
        goal.goal.goal = goal_name
        # print(goal)
        self.pub.publish(goal)

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
                    time.sleep(1)
                    break

    def restart():
        # print(script_path)
        try:
            # 使用 subprocess.run 執行指令
            # result = subprocess.run(script_path, shell=True, capture_output=True, text=True)
            subprocess.Popen([script_path])
            # subprocess.Popen([sys.executable, python_path])

            
            # 判斷是否執行成功
            # if result.returncode == 0:
            #     print("Command executed successfully.")
            #     print(f"Output:\n{result.stdout}")  # 輸出結果
            # else:
            #     print("Command failed with return code:", result.returncode)
            #     print(f"Error message:\n{result.stderr}")   # 錯誤訊息
        except Exception as e:
            print("An error occurred while running the command:", e)
        # pass

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
    project_path = os.path.dirname(os.path.dirname(__file__))
    window = MainWindow()
    Btn = BtnPush()
    btn_function = {btn_text[0][0]:Btn.p1, btn_text[1][0]:Btn.p2, btn_text[0][1]:Btn.close, btn_text[1][1]:Btn.reset}
    window.menu_ui()
    script_path = project_path + "/Script/restart_script.sh"
    music_path = project_path + "/music/Free_Music.mp3"
    player = NavigationPlayMusic()
    # print(script_path)
    window.show()
    sys.exit(app.exec_())
    # while app.exec_(): pass
    # rospy.signal_shutdown("GUI is shutdown")          
    # sys.exit()
