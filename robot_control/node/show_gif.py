#!/usr/bin/env python3
import sys, os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
from password import PasswordCheckApp

class FullscreenGIF(QWidget):
    def __init__(self, gif_path):
        super().__init__()
        self.password_gui = PasswordCheckApp(app.primaryScreen().availableGeometry(), app.primaryScreen().physicalDotsPerInch(), project_path)
        self.password_gui.closed.connect(self.PasswordCloseEven)
        self.initUI(gif_path)
    
    def initUI(self, gif_path):
        layout = QVBoxLayout()
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        
        screen_size = QApplication.primaryScreen().size()
        self.movie.setScaledSize(QSize(screen_size.width(), screen_size.height()))
        
        self.movie.start()
        
        self.setStyleSheet("background-color: black;")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def mousePressEvent(self, event): # 當觸碰畫面時執行
        # self.close()
        self.password_gui.access = False
        self.password_gui.show()

    def PasswordCloseEven(self): # 當密碼鎖的gui關閉時執行
        if self.password_gui.access:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # project_path = os.path.dirname(os.path.dirname(__file__)) #得到專案路徑
    project_path = "/home/ericlai/project/gui_ws/src/robot_control"
    gif_path = project_path + "/screen_image/1742019751952.gif"  # GIF 檔案路徑
    player = FullscreenGIF(gif_path)
    player.show()
    sys.exit(app.exec_())
