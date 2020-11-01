# 主程序的按键模块设计
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
import sys

from PyQt5.QtCore import *

class MyButton(QLabel):


    clicked = pyqtSignal()#自定义一个信号

    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.hoverPixmap = QPixmap(args[0])
        self.normalPixmap = QPixmap(args[1])
        self.pressPixmap = QPixmap(args[2])

        self.enterState = False
        self.setPixmap(self.normalPixmap)
        self.setFixedSize(self.normalPixmap.size())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if self.enterState == False:
            self.setPixmap(self.normalPixmap)
        else:
            self.setPixmap(self.hoverPixmap)

        self.clicked.emit()#发射信号


    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.setPixmap(self.pressPixmap)

    def enterEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.hoverPixmap)
        self.enterState = True

    def leaveEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.normalPixmap)
        self.enterState = False


if __name__ == '__main__':
    a = QApplication(sys.argv)
    mybtn = MyButton('source/人机对战_hover.png',
                     'source/人机对战_normal.png',
                     'source/人机对战_press.png')
    mybtn.show()
    sys.exit(a.exec_())
