#!/usr/bin/env python3
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
from password import PasswordCheckApp

class FullscreenGIF(QtWidgets.QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.password_gui = PasswordCheckApp(app.primaryScreen().availableGeometry(), app.primaryScreen().physicalDotsPerInch(), project_path)
        self.password_gui.closed.connect(self.PasswordCloseEven)
        self.gif_path = project_path + "/screen_image/1742019751952.gif"  # GIF 檔案路徑
        self.initUI()
    
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        
        self.movie = QMovie(self.gif_path)
        self.label.setMovie(self.movie)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        
        screen_size = QtWidgets.QApplication.primaryScreen().size()
        self.movie.setScaledSize(QSize(screen_size.width(), screen_size.height()))
        
        self.movie.start()
        
        self.setStyleSheet("background-color: black;")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def mousePressEvent(self, even): # 當觸碰畫面時執行
        # self.close()
        self.password_gui.access = False
        self.password_gui.exec_()

    def PasswordCloseEven(self): # 當密碼鎖的gui關閉時執行
        if self.password_gui.access: # 如果密碼輸入正確就關閉螢幕保護視窗
            self.close()
        
        self.password_gui.init_content() # reset內容

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path = "/home/ericlai/project/gui_ws/src/robot_control"
    player = FullscreenGIF(path)
    player.show()
    sys.exit(app.exec_())
