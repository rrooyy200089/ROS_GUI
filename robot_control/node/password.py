#!/usr/bin/env python3

import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from time import sleep

class PasswordCheckApp(QtWidgets.QWidget):
    closed = pyqtSignal()   # 建立signal,讓外部程式可以接收到關閉事件
    def __init__(self, screen_size, screen_dpi, project_path):
        super().__init__()
        self.correct_password = "1234"  # 設定正確的密碼
        self.entered_password = ""
        self.btn = [None for _ in range(12)] # 12個按鍵
        # self.screen = app.primaryScreen().availableGeometry() # 得到畫面可以顯示範圍
        self.project_path = project_path
        self.screen = screen_size
        self.dpi = screen_dpi
        self.access = False # 是否解鎖
        self.initUI()
    
    def initUI(self):
        display_width, display_height = int(self.screen.height()//1.7), int(self.screen.height()-10)
        self.display_button_size = int(display_width / 3.3)
        # dpi = int(app.primaryScreen().physicalDotsPerInch())
        # dpi = screen_dpi


        main_layout = QtWidgets.QVBoxLayout()

        # 標題
        self.label = QtWidgets.QLabel()
        pixmap = QPixmap(self.project_path + "/icon/lock.png")  # 載入圖片
        self.picture_size = 70 * self.dpi // 141
        scaled_pixmap = pixmap.scaled(self.picture_size, self.picture_size, aspectRatioMode=Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setScaledContents(True)
        main_layout.addWidget(self.label)
        
        # 輸入顯示
        self.password_label = QtWidgets.QLabel()
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setFont(QFont("Arial", 50*self.dpi//141))
#         self.password_label.setStyleSheet("""
#     QLabel {
#         border: 2px solid black;
#         padding: 5px;
#     }
# """)
        self.password_label.setFixedHeight(70*self.dpi//141)
        self.update_display()
        main_layout.addWidget(self.password_label)

        # 提示警告
        self.hint_label = QtWidgets.QLabel()
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setFont(QFont('標楷體', 30*self.dpi//141))
        self.hint_label.setStyleSheet("color:#f00;")
        self.hint_label.setFixedHeight(70*self.dpi//141)
        main_layout.addWidget(self.hint_label)
        
        # 鍵盤
        grid_layout = QtWidgets.QGridLayout()
        # 數字
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for i, num in enumerate(numbers):
            self.btn[i] = QtWidgets.QPushButton(num)
            # button.setFont(QFont("Arial", 70))
            self.btn[i].setFixedSize(self.display_button_size, self.display_button_size)
            self.btn[i].setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid black;
                    border-radius: {self.display_button_size//2}px;   /* 一半的尺寸就是圓 */
                    background-color: white;
                    font-size: {int(self.display_button_size//1.5)}px;
                }}
            """)
            self.btn[i].pressed.connect(lambda key=i : self.btn_pressed(key))
            self.btn[i].released.connect(lambda n=num, key=i : self.add_digit(n, key))
            grid_layout.addWidget(self.btn[i], i // 3, (i % 3) if num != "0" else 1)

        # 返回
        self.btn[10] = QtWidgets.QPushButton() 
        self.btn[10].setFixedSize(self.display_button_size, self.display_button_size)
        self.btn[10].setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: {self.display_button_size//2}px;
                border: none;
            }}""")
        icon = QIcon(QPixmap(self.project_path + "/icon/back-arrow.png"))
        self.btn[10].setIcon(icon)
        self.btn[10].setIconSize(self.btn[10].size()*0.7)
        self.btn[10].pressed.connect(lambda key=10 : self.btn_pressed(key))
        self.btn[10].released.connect(self.back)
        grid_layout.addWidget(self.btn[10], 3, 0)
        
        # 刪除
        self.btn[11] = QtWidgets.QPushButton() 
        self.btn[11].setFixedSize(self.display_button_size, self.display_button_size)
        self.btn[11].setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: {self.display_button_size//2}px;
                border: none;
            }}""")
        icon = QIcon(QPixmap(self.project_path + "/icon/backspace.png"))
        self.btn[11].setIcon(icon)
        self.btn[11].setIconSize(self.btn[11].size()*0.7)
        self.btn[11].pressed.connect(lambda key=11 : self.btn_pressed(key))
        self.btn[11].released.connect(self.delete_digit)
        grid_layout.addWidget(self.btn[11], 3, 2)
        

        main_layout.addLayout(grid_layout)
        
        self.setLayout(main_layout)
        self.setWindowFlags(Qt.FramelessWindowHint) 
        # self.setWindowTitle("密碼輸入")
        self.setFixedSize(display_width, display_height)
        # self.show()

    def btn_pressed(self, key):
        if key < 10:
            self.btn[key].setStyleSheet(f"""
                    QPushButton {{
                        border: 2px solid black;
                        border-radius: {self.display_button_size//2}px;   /* 一半的尺寸就是圓 */
                        background-color: yellow;
                        font-size: {int(self.display_button_size//1.5)}px;
                    }}
                """)
        
        else :
            self.btn[key].setStyleSheet(f"""
                QPushButton {{
                    background-color: yellow;
                    border-radius: {self.display_button_size//2}px;
                    border: none;
                }}""")
            
        self.btn[key].repaint()
        sleep(0.1)
    
    def add_digit(self, digit, key):
        self.btn[key].setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid black;
                    border-radius: {self.display_button_size//2}px;   /* 一半的尺寸就是圓 */
                    background-color: white;
                    font-size: {int(self.display_button_size//1.5)}px;
                }}
            """)
        self.hint_label.setText("")
        if len(self.entered_password) < 4:
            self.entered_password += digit
            self.update_display()
        
        if len(self.entered_password) == 4:
            self.check_password()

    def back(self):
        self.btn[10].setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: {self.display_button_size//2}px;
                border: none;
            }}""")
        self.btn[10].repaint()
        sleep(0.5)
        self.close()
    
    def delete_digit(self):
        self.btn[11].setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: {self.display_button_size//2}px;
                border: none;
            }}""")
        self.entered_password = self.entered_password[:-1]
        self.update_display()
    
    def update_display(self):
        label_text = ""
        for i in range(4):
            label_text += "●" if i < len(self.entered_password) else "○"
            label_text += "     " if i < 3 else ""
        # self.label.setText("●" * len(self.entered_password) + "○" * (4 - len(self.entered_password)))
        self.password_label.setText(label_text)
        self.password_label.repaint() # 強制立即更新
    
    def check_password(self):
        if self.entered_password == self.correct_password:
            pixmap = QPixmap(self.project_path + "/icon/unlock.png")  # 載入圖片
            scaled_pixmap = pixmap.scaled(self.picture_size, self.picture_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.label.setPixmap(scaled_pixmap)
            # self.label.setAlignment(Qt.AlignCenter)
            self.label.repaint()
            self.access = True
            sleep(0.6)
            self.close()
        else:
            self.hint_label.setText("密碼錯誤！")
            sleep(0.2)
            self.entered_password = ""
            self.update_display()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    project_path = os.path.dirname(os.path.dirname(__file__))   #得到專案路徑
    size = app.primaryScreen().availableGeometry()  # 得到畫面可以顯示的範圍
    dpi = int(app.primaryScreen().physicalDotsPerInch())    # 得到畫面的dpi
    ex = PasswordCheckApp(size, dpi, project_path)
    ex.show()
    sys.exit(app.exec_())