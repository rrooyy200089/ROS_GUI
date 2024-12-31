#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtCore import QRect
import rospy
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from forklift_server.msg import TopologyMapActionGoal
import subprocess, time, os
from std_msgs.msg import Bool, Float64
import threading
# from process import Process 

btn_text = [['急診室門口', '結束'], ['藥局', '重新啟動']]
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
        self.msg_window = MessageWindow()
        self.yesno_window = YesNoWindow()
        self.btn = [[None] * 3 for _ in range(2)]
        rospy.Subscriber("/car_voltage", Float64, self.get_car_power, queue_size=1)
        self.car_power = 0
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
                self.btn[i][j].setFont(QtGui.QFont('標楷體', 40)) #70
                # self.btn[i][j].setStyleSheet('''
                #                              font-size:40px;
                #                              ''')
                self.btn[i][j].setFixedSize(int((self.box.width()-15)/col_num), int((self.box.height()-15)/row_num))
                # self.btn[i][j].clicked.connect(btn_function[btn_text[i][j]])
                self.btn[i][j].pressed.connect(lambda x=i, y=j: Btn.btn_pressed(x, y))  # 當按鈕"按下"時，所要執行的函式
                self.btn[i][j].released.connect(btn_function[btn_text[i][j]]) # 當按鈕"放開"時，所要執行的函式
                self.grid.addWidget(self.btn[i][j], i, j, QtCore.Qt.AlignCenter)

    def get_car_power(self, msg):
        self.car_power = msg.data
        if self.car_power < 26 and self.car_enable:
            # QtCore.QMetaObject.invokeMethod(self, "message_display", QtCore.Qt.QueuedConnection)
            QtCore.QTimer.singleShot(0, self.message_display)
            # QtCore.QTimer.singleShot(0, lambda text = "沒電":self.message_display(message_text=text))
            # self.message_display()
            self.car_enable = False

    def message_display(self):
        mbox = QtWidgets.QWidget()
        mbox.resize(1400, 900)

        mgrid = QtWidgets.QGridLayout(mbox)

        lab_icon = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(800, 800)
        lab_icon.setPixmap(scaled_pixmap)
        mgrid.addWidget(lab_icon, 0, 0)

        lab = QtWidgets.QLabel(self)
        lab.setText("沒電")
        lab.setFont(QtGui.QFont('Verdana', 90))
        mgrid.addWidget(lab, 0, 1)

        mbtn = QtWidgets.QPushButton(self)
        mbtn.setText("OK")          
        mbtn.setStyleSheet('''
                        QPushButton{
                        min-height:300px;   
                        }
                            ''')
        mgrid.addWidget(mbtn, 1, 1)
        mbox.show()

        # # self.mbox.warning(self, "車子低電量警告", f"車子電量過低({msg.data}V)\n請先充電")
        # mbox = QtWidgets.QMessageBox(self)
        # # mbox.resize(2300, 900)
        # # mbox.setGeometry(0, 0, 2000, 900)
        # # print("Screen width:", mbox.width(), "Screen height:", mbox.height())
        # mbox.setStyleSheet('''
        #             QLabel{
        #             font-size:600px;
        #             font-weight:bold;
        #             text-align:center;
        #             color:red;
        #             min-height:900px;
        #             min-width: 2000px;
        #             }
        #             QPushButton{
        #             font-size:80px;
        #             min-height:120px;
        #             max-height:120px;
        #             min-width: 240px;
        #             max-width: 240px;
        #             icon-size: 70px;
        #             }
        #             ''')    # 設定MessageBox的顯示樣式
        # mbox.setIcon(QtWidgets.QMessageBox.Warning)
        # mbox.setWindowTitle("車子低電量警告")
        # mbox.setText("沒電")
        # ret = mbox.exec_()
        # return ret

    # def show(self):
    #     self.show()

    # def closeEvent(self, self.form.event):
        # pass

class MessageWindow(QtWidgets.QDialog):
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
        # self.setGeometry((self.screen.width()/2)-(self.window_width/2), (self.screen.height()/2)-(self.window_height/2), self.window_width, self.window_height)
        self.ui()
        # print(f"svodnv  {app.primaryScreen().physicalDotsPerInch()}")

    def ui(self):
        mbox = QtWidgets.QWidget(self)
        mbox.setGeometry(0, 0, self.width()-10, self.height()-10)
        # # mbox.setGeometry(10, 10, 1400, 900)
        # print(f"vjskdbvu : {mbox.width()}")
        mgrid = QtWidgets.QGridLayout(mbox)

        # background_color = self.palette().color(self.backgroundRole())  # 得到視窗的背景顏色
        # color_name = background_color.name()  # 得到顏色的名稱

        lab_icon = QtWidgets.QLabel(self)
        lab_icon_size = int(750*self.dpi//188)
        lab_icon.resize(lab_icon_size, lab_icon_size)
        # lab_icon.setStyleSheet(f'''QLabel{{border : 2px solid {color_name};}}''')  # 將icon的邊框設成更背景顏色一樣，以便隱藏邊框
        pixmap = QtGui.QPixmap(image_path)
        pixmap_size = int(750*self.dpi//188)
        scaled_pixmap = pixmap.scaled(pixmap_size, pixmap_size)
        lab_icon.setPixmap(scaled_pixmap)
        lab_icon.setAlignment(QtCore.Qt.AlignCenter)
        mgrid.addWidget(lab_icon, 0, 0)

        lab = QtWidgets.QLabel(self)
        lab.setStyleSheet(f'''
                          QLabel{{
                          font-weight:bold;
                          color:red;  
                          }}''')
        lab.setText("沒電")
        lab.setFont(QtGui.QFont('標楷體', int(300*self.dpi//188)))
        lab.setAlignment(QtCore.Qt.AlignCenter)
        mgrid.addWidget(lab, 0, 1)

        mbtn = QtWidgets.QPushButton(self)
        mbtn.setText("OK")
        check_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        mbtn.setIcon(check_icon) 
        mbtn.setStyleSheet(f'''
                           QPushButton{{
                           font-size:{int(200*self.dpi//188)}px;
                           min-height:{int(300*self.dpi//188)}px;
                           }}''')
        mbtn.setIconSize(mbtn.size() * 5)
        mbtn.clicked.connect(self.btn)         
        mgrid.addWidget(mbtn, 1, 0, 1, 2)
        
    def btn(self):
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
        self.ui()

    def ui(self):
        box = QtWidgets.QWidget(self)
        box.setGeometry(0, 0, self.width()-10, self.height()-10)

        grid = QtWidgets.QGridLayout(box)
        
        Ybtn = QtWidgets.QPushButton(self)
        Ybtn.setText("Yes")
        Ybtn.setObjectName("Yes")
        yes_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        Ybtn.setIcon(yes_icon)
        Ybtn.setStyleSheet(f'''
                           QPushButton{{
                           font-size:{int(300*self.dpi//188)}px;
                           min-height:{box.height()}px;
                           }}''')
        Ybtn.setIconSize(Ybtn.size() * 6)
        Ybtn.clicked.connect(self.accept)
        grid.addWidget(Ybtn, 0, 0)

        Nbtn = QtWidgets.QPushButton(self)
        Nbtn.setText("No")
        Nbtn.setObjectName("No")
        no_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton)
        Nbtn.setIcon(no_icon)
        Nbtn.setStyleSheet(f'''
                           QPushButton{{
                           font-size:{int(300*self.dpi//188)}px;
                           min-height:{box.height()}px;
                           }}''')
        Nbtn.setIconSize(Nbtn.size() * 6)
        Nbtn.clicked.connect(self.reject)
        grid.addWidget(Nbtn, 0, 1)


class BtnPush():
    def __init__(self):
        self.pub = rospy.Publisher("/TopologyMap_server/goal", TopologyMapActionGoal, queue_size=1, latch=True)

    def btn_pressed(self, x, y):        # 當按鈕按下時，會根據回傳的x, y值，將所對應的按鈕背景顏色改成黃色
        # print(f"x:{x} y:{y}")
        window.btn[x][y].setStyleSheet("background-color : yellow")

    def p1(self):
        window.btn[0][0].setStyleSheet("background-color : lightgray")
        # window.message_display()
        window.msg_window.exec_()
        if(window.car_enable):
            self.pub_goal(goal_name='P11')
        else :
            # window.message_display(icon_style=QtWidgets.QMessageBox.Warning, message_title="車子低電量警告", message_text=f"車子電量過低({window.car_power}V)\n請先充電")
            window.message_display()

        # print("P1")
        # player.play_music()
    
    def p2(self):
        window.btn[1][0].setStyleSheet("background-color : lightgray")
        ret = window.yesno_window.exec_()
        print('Yes' if ret == QtWidgets.QDialog.Accepted else "N0")
        if(window.car_enable):
            self.pub_goal(goal_name='P6')
        else :
            # window.message_display(icon_style=QtWidgets.QMessageBox.Warning, message_title="車子低電量警告", message_text=f"車子電量過低({window.car_power}V)\n請先充電")
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
        window.btn[0][1].setStyleSheet("background-color : lightgray")
        # ret = window.message_display(icon_style=QtWidgets.QMessageBox.Question, message_title="動作確認", message_text="您確定要關閉程式嗎？")
        # if ret == QtWidgets.QMessageBox.No : return
        # time.sleep(1)
        param = '-15'
        enable = False
        while True:
            process = Process.find_process()
            if len(process) <= 1 and enable: break
            elif enable: param = '-9', print("Closing not completed yet!!!")
            Process.close(ros_process=process, kill_param=param)
            time.sleep(1)
            enable = True
        print("close")

    def reset(self):
        window.btn[1][1].setStyleSheet("background-color : lightgray")
        # ret = window.message_display(icon_style=QtWidgets.QMessageBox.Question, message_title="動作確認", message_text="您確定要重新啟動程式嗎？")
        # if ret == QtWidgets.QMessageBox.No : return
        # c = threading.Thread(target=self.close())
        # c.daemon = True
        # r = threading.Thread(target=Process.restart())
        # r.daemon = True
        # if os.path.exists(script_path):  # 判斷檔案是否存在
        #     self.close()
        #     # c.start()
        #     # Process.restart()
        #     # c.start()
        #     # c.join()
        #     time.sleep(2)
        #     r = threading.Thread(target=Process.restart())
        #     r.daemon = True
        #     r.start()
        # else :
        #     print('No such file !!')
        print("reset")

    def pub_goal(self, goal_name=''):
        goal = TopologyMapActionGoal()
        goal.goal.goal = goal_name
        # print(goal)
        self.pub.publish(goal)

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
    image_path = os.path.dirname(os.path.dirname(__file__)) + "/node/warning_big.png"
    window = MainWindow()
    Btn = BtnPush()
    btn_function = {btn_text[0][0]:Btn.p1, btn_text[1][0]:Btn.p2, btn_text[0][1]:Btn.close, btn_text[1][1]:Btn.reset}
    window.menu_ui()
    script_path = os.path.dirname(os.path.dirname(__file__)) + "/Script/restart_script.sh"
    music_path = os.path.dirname(os.path.dirname(__file__)) + "/music/Free_Music.mp3"
    python_path = os.path.dirname(os.path.dirname(__file__)) + "/node/restart_process.py"
    player = NavigationPlayMusic()
    # print(script_path)
    window.show()
    sys.exit(app.exec_())
    # while app.exec_(): pass
    # rospy.signal_shutdown("GUI is shutdown")          
    # sys.exit()
