#!/usr/bin/env python3
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
from password import PasswordCheckApp

class FullscreenGIF(QtWidgets.QWidget):
    def __init__(self, parent, screen_size, screen_dpi, project_path):
        super().__init__(parent)
        self.password_gui = PasswordCheckApp(screen_size, screen_dpi, project_path)
        self.gif_path = project_path + "/screen_image/1744695714913.gif"  # GIF 檔案路徑
        # self.screen = screen_size
        self.screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.initUI()
    
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setStyleSheet(""" 
        #     QLabel {
        #         border: 2px solid white;
        #         padding: 5px;
        #     }
        # """) # 顯示邊框
        self.movie = QMovie(self.gif_path)
        self.label.setMovie(self.movie)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.SplashScreen)
        self.setGeometry(self.screen) # 強制視窗設定為螢幕的大小

        self.movie.setScaledSize(self.screen.size()*1.0)
        self.label.setFixedSize(self.screen.size())
                
        self.setStyleSheet("background-color: black;")

        self.setCursor(Qt.BlankCursor) # 設定不要顯示游標
        
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Escape:
    #         self.close()
    
    def mousePressEvent(self, even): # 當觸碰畫面時執行
        self.password_gui.access = False
        self.password_gui.exec_()
        if self.password_gui.access: # 如果密碼輸入正確就關閉螢幕保護視窗
            self.close()
            if not self.parent() == None : self.parent().resume_timer()
        self.password_gui.init_content() # reset內容

    def showGIF(self):
        self.showFullScreen()   # 全螢幕
        self.movie.start()      # GIF開始動

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    size = app.primaryScreen().availableGeometry()  # 得到畫面可以顯示的範圍
    dpi = int(app.primaryScreen().physicalDotsPerInch())    # 得到畫面的dpi
    path = "/home/ericlai/project/gui_ws/src/robot_control"
    player = FullscreenGIF(None, size, dpi, path)
    # player.movie.start()
    # player.showFullScreen()
    player.showGIF()
    sys.exit(app.exec_())
