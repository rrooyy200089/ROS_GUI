#!/usr/bin/env python3

import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from time import sleep

class PasswordCheckApp(QtWidgets.QDialog):
    def __init__(self, screen_size, screen_dpi, project_path):
        super().__init__()
        self.correct_password = "1234"  # 設定正確的密碼
        self.entered_password = ""
        self.btn = [None for _ in range(12)] # 12個按鍵
        self.project_path = project_path
        self.screen = screen_size
        self.dpi = screen_dpi
        self.access = False # 是否解鎖
        self.timer = QTimer(self)   # 設定顯示"Error"文字的時間
        self.timer.setInterval(3000)    # 3秒
        self.initUI()
    
    def initUI(self):
        display_width, display_height = int(self.screen.height()*1.5), int(self.screen.height()-50*self.dpi//188)
        self.display_button_width_size = int(display_width / 4.2)

        # 設定成垂直顯示
        main_layout = QtWidgets.QVBoxLayout()

        # 水平顯示內容(message & icon)
        level_main_layout = QtWidgets.QHBoxLayout()

        # 狀態icon
        self.state_label = QtWidgets.QLabel()
        picture_size = 250 * self.dpi // 188
        lock_pixmap = QPixmap(self.project_path + "/icon/lock.png") # 載入鎖上的圖片
        unlock_pixmap = QPixmap(self.project_path + "/icon/unlock.png")  # 載入解鎖的圖片
        self.scaled_lock_pixmap = lock_pixmap.scaled(picture_size, picture_size, aspectRatioMode=Qt.KeepAspectRatio) # 調整圖片尺寸
        self.scaled_unlock_pixmap = unlock_pixmap.scaled(picture_size, picture_size, aspectRatioMode=Qt.KeepAspectRatio) # 調整圖片尺寸
        self.state_label.setPixmap(self.scaled_lock_pixmap)
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setFixedSize((500*self.dpi//188), (270*self.dpi//188))
        # self.state_label.setStyleSheet("""
        #     QLabel {
        #         border: 2px solid black;
        #         padding: 5px;
        #     }
        # """) # 顯示邊框
        level_main_layout.addWidget(self.state_label)
        
        # 輸入顯示("●" or "○" ＆ Message)
        self.password_label = QtWidgets.QLabel()
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setFont(QFont("Times New Roman", 120*self.dpi//188))
        # self.password_label.setStyleSheet("""
        #     QLabel {
        #         border: 2px solid black;
        #         padding: 5px;
        #     }
        # """) # 顯示邊框
        self.password_label.setFixedHeight(self.state_label.height())
        self.update_display()
        level_main_layout.addWidget(self.password_label)

        # 無顯示(幫助調整位置用的)
        self.label = QtWidgets.QLabel()
        self.label.setFixedWidth(150*self.dpi//188)
        # self.label.setStyleSheet(""" 
        #     QLabel {
        #         border: 2px solid black;
        #         padding: 5px;
        #     }
        # """) # 顯示邊框
        level_main_layout.addWidget(self.label)

        main_layout.addLayout(level_main_layout)

        # 鍵盤
        grid_layout = QtWidgets.QGridLayout()
        # 數字
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for i, num in enumerate(numbers):
            self.btn[i] = QtWidgets.QPushButton(num)
            # self.btn[i].setFixedSize(self.display_button_size, self.display_button_size)
            self.btn[i].setFixedWidth(self.display_button_width_size)
            self.btn[i].setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid black;
                    background-color: white;
                    font-size: {int(self.display_button_width_size//1.7)}px;
                }}
            """)
            self.btn[i].pressed.connect(lambda key=i : self.btn_pressed(key))
            self.btn[i].released.connect(lambda n=num, key=i : self.add_digit(n, key))
            grid_layout.addWidget(self.btn[i], i // 4, i % 4)

        # 刪除鍵
        self.btn[10] = QtWidgets.QPushButton() 
        self.btn[10].setFixedWidth(self.display_button_width_size)
        self.btn[10].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid black;
                background-color: white;
            }}""")
        icon = QIcon(QPixmap(self.project_path + "/icon/backspace.png"))
        self.btn[10].setIcon(icon)
        self.btn[10].setIconSize(self.btn[10].size()*0.68)
        self.btn[10].pressed.connect(lambda key=10 : self.btn_pressed(key))
        self.btn[10].released.connect(self.delete_digit)
        grid_layout.addWidget(self.btn[10], 2, 2)
        
        # 返回鍵
        self.btn[11] = QtWidgets.QPushButton() 
        self.btn[11].setFixedWidth(self.display_button_width_size)
        self.btn[11].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid black;
                background-color: white;
            }}""")
        icon = QIcon(QPixmap(self.project_path + "/icon/back-arrow.png"))
        self.btn[11].setIcon(icon)
        self.btn[11].setIconSize(self.btn[11].size()*0.68)
        self.btn[11].pressed.connect(lambda key=11 : self.btn_pressed(key))
        self.btn[11].released.connect(self.back)
        grid_layout.addWidget(self.btn[11], 2, 3)        

        main_layout.addLayout(grid_layout)
        
        self.setLayout(main_layout)
        self.setWindowFlags(Qt.FramelessWindowHint) # 移除整個視窗的標題列與邊框，但不能用這個方法，因為在開啟時點擊主視窗會觸發 Ubuntu 的 bug
        # self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # 將視窗設定成"沒有標題列"的畫面視窗，並永遠保持在最上層，以免在點擊主視窗時不會跳焦
        self.setFixedSize(display_width, display_height)
        self.move((self.screen.width()-display_width)//2, (self.screen.height()-display_height)//2) # 將視窗移到畫面中間
        self.timer.timeout.connect(self.recover_display)
        # self.show()

    def btn_pressed(self, key):
        self.btn[key].setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid black;
                    background-color: yellow;
                    font-size: {int(self.display_button_width_size//1.7)}px;
                }}
            """)          
        self.btn[key].repaint()
        sleep(0.1)
    
    def add_digit(self, digit, key):
        self.btn[key].setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid black;
                    background-color: white;
                    font-size: {int(self.display_button_width_size//1.7)}px;
                }}
            """)
        if len(self.entered_password) < 4:
            self.entered_password += digit
            self.update_display()
        
        if len(self.entered_password) == 4:
            self.check_password()

    def back(self):
        self.btn[11].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid black;
                background-color: white;
            }}""")
        self.btn[11].repaint()
        sleep(0.1)
        self.close()
    
    def delete_digit(self):
        self.btn[10].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid black;
                background-color: white;
            }}""")
        self.entered_password = self.entered_password[:-1]
        self.update_display()
    
    def update_display(self):
        if self.timer.isActive() : self.timer.stop()
        password_label_text = ""
        for i in range(4):
            password_label_text += "●" if i < len(self.entered_password) else "○"
            password_label_text += "     " if i < 3 else ""
        # self.label.setText("●" * len(self.entered_password) + "○" * (4 - len(self.entered_password)))
        self.password_label.setStyleSheet("""color:black;""")
        self.password_label.setText(password_label_text)
        self.password_label.repaint() # 強制立即更新
    
    def check_password(self):
        if self.entered_password == self.correct_password:
            self.state_label.setPixmap(self.scaled_unlock_pixmap)
            self.password_label.setText("P A S S")
            self.password_label.setStyleSheet("""color:#00CC00;font-weight: bold;""") # 稍暗的亮綠色
            self.state_label.repaint()
            self.password_label.repaint()
            self.access = True
            sleep(0.6)
            self.close()
        else:
            self.password_label.setText("E R R O R")
            self.password_label.setStyleSheet("""color:red;font-weight: bold;""")
            self.password_label.repaint()
            self.entered_password = ""
            self.timer.start()  # 開始計時3秒

    def recover_display(self):
        self.update_display()

    def init_content(self):
        self.entered_password = ""
        self.update_display()
        self.state_label.setPixmap(self.scaled_lock_pixmap)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path = "/home/ericlai/project/gui_ws/src/robot_control"
    size = app.primaryScreen().availableGeometry()  # 得到畫面可以顯示的範圍
    dpi = int(app.primaryScreen().physicalDotsPerInch())    # 得到畫面的dpi
    ex = PasswordCheckApp(size, dpi, path)
    ex.show()
    sys.exit(app.exec_())