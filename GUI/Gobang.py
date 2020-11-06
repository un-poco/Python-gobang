from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
sys.path.append("D:/Pyfiles/PY_gobang/AI")
sys.path.append('D:/Git/PY_gobang/GUI/double_play')
import MyButton
import gobangGUI
import doublePlayerGUI
sys.path.append("D:\Pyfiles\PY_gobang\AI")

import MyButton
import gobangGUI

import numpy as np

class Mainwindow(QWidget):

    def __init__(self,parent = None):
        super().__init__(parent)
        self.resize(760,650)
        self.setWindowTitle("gobang")
        #设置窗口图标
        self.setWindowIcon(QIcon("source/icon.ico"))



        #设置背景图片
        p = QPalette(self.palette())#获得当前的调色板
        brush = QBrush(QImage("source/gobang_background.png"))
        p.setBrush(QPalette.Background,brush)#设置调色版
        self.setPalette(p)#给窗口设置调色板


        self.singlePlayerBtn = MyButton.MyButton('source/人机对战_hover.png',
                     'source/人机对战_normal.png',
                     'source/人机对战_press.png',
                     parent=self)
        self.singlePlayerBtn.move(250, 450)

        self.doublePlayerBtn = MyButton.MyButton('source/双人对战_hover.png',
                     'source/双人对战_normal.png',
                     'source/双人对战_press.png',
                     parent=self)
        self.doublePlayerBtn.move(250,500)

        #绑定开始双人游戏信号和槽函数
        self.doublePlayerBtn.clicked.connect(self.startDoubleGame)
        self.singlePlayerBtn.clicked.connect(self.startSingleGame)


    def startDoubleGame(self):
        #构建双人对战界面

        self.doublePlayerGame = doublePlayerGUI.GoBang()

        #绑定返回界面
        self.doublePlayerGame.backSignal.connect(self.showStartGame)
        
        self.doublePlayerGame.show()#显示游戏界面
        self.close()


    def startSingleGame(self):
        self.SingleGame = gobangGUI.GoBang()
        #self.SingleGame = SinglePlayerGame.SinglePlayerGame()
        self.SingleGame.backSignal.connect(self.showStartGame2)
        self.SingleGame.show()
        self.close()

    #显示开始界面
    def showStartGame(self):
        self.show()
        self.doublePlayerGame.close()

    def showStartGame2(self):
        self.show()
        self.SingleGame.close()

    

if __name__ == "__main__":
    import cgitb

    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = Mainwindow()
    m.show()
    sys.exit(a.exec_())
