'''
    这是白嫖的人人代码，对接的同学可以看一下。被我魔改了所以落子和按钮是歪的。
'''

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import numpy as np

class Chessman(QLabel):

    def __init__(self, color = "black",parent = None):
        super().__init__(parent)
        self.color = color
        self.pic = None
        if self.color == "black":
            self.pic = QPixmap("source/黑子.png")
        else:
            self.pic = QPixmap("source/白子.png")
        self.setPixmap(self.pic)
        self.setFixedSize(self.pic.size())#设置棋子大小
        self.show()

        self.x = 0
        self.y = 0

    def move(self,a0:QtCore.QPoint):
        super().move(a0.x()-15,a0.y()-15)

    def setIndex(self,x,y):
        self.x = x
        self.y = y

import MyButton

class DoublePlayGame(QWidget):
    
    backSignal = pyqtSignal()#返回信号
    def __init__(self,parent = None):
        super().__init__(parent=parent)
        #左上角chessboard[0][0]
        #右上角chessboard[0][18]
        #左下角chessboard[18][0]
        #右下角chessboard[18][18]
        #chessboard[行下标][列下标]
        self.chessboard = [[None for i in range(16)] for i in range(16)]
        #落子棋子颜色
        self.turnChessColor = "black"
        self.history = []
        self.history2 = []
        self.is_over = False

        #配置背景图
        p = QPalette(self.palette())#获得当前的调色板
        brush = QBrush(QImage("source/游戏界面.png"))
        p.setBrush(QPalette.Background,brush)#设置调色版
        self.setPalette(p)#给窗口设置调色板

        #设置标题
        #self.resize(760,650)
        self.setWindowTitle("双人联机")

        #设置窗口图标
        self.setWindowIcon(QIcon("source/icon.ico"))
        #设置窗口大小
        self.setFixedSize(QImage("source/游戏界面.png").size())

        self.backBtn = MyButton.MyButton('source/返回按钮_hover.png',
                     'source/返回按钮_normal.png',
                     'source/返回按钮_press.png',
                     parent=self)
        self.backBtn.move(650,50)

        self.startBtn = MyButton.MyButton('source/开始按钮_hover.png',
                     'source/开始按钮_normal.png',
                     'source/开始按钮_press.png',
                     parent=self)
        self.startBtn.move(650,300)

        self.returnBtn = MyButton.MyButton('source/悔棋按钮_hover.png',
                     'source/悔棋按钮_normal.png',
                     'source/悔棋按钮_press.png',
                     parent=self)
        self.returnBtn.move(650,400)

        self.loseBtn = MyButton.MyButton('source/认输按钮_hover.png',
                     'source/认输按钮_normal.png',
                     'source/认输按钮_press.png',
                     parent=self)
        self.loseBtn.move(650,500)

        #绑定返回按钮
        self.backBtn.clicked.connect(self.goBack)
        self.startBtn.clicked.connect(self.restar)
        self.loseBtn.clicked.connect(self.lose)
        self.returnBtn.clicked.connect(self.huiback)

        self.gameStatu = []

        self.focusPoint = QLabel(self)
        self.focusPoint.setPixmap(QPixmap("source/标识.png"))

    def goBack(self):
        self.backSignal.emit()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.backSignal.emit()




    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.gameStatu == False:
            return None
        print(a0.pos())
        print("x:",a0.x())
        print("y:",a0.y())
        pos,chess_index = self.reversePos(a0)
        if pos is None:
            return

        if self.chessboard[chess_index[1]][chess_index[0]] != None:
            return

        
        self.chess = Chessman(color=self.turnChessColor,parent=self)
        self.chess.setIndex(chess_index[0], chess_index[1])
        self.chess.move(pos)
        self.chess.show()#显示棋子
        self.history.append(self.chess)
        self.history2.append(self.focusPoint)

        self.focusPoint.move(QPoint(pos.x()-15,pos.y()-15))
        self.focusPoint.show()
        self.focusPoint.raise_()

        print("棋盘交点位置：",chess_index)

        #放入棋盘
        self.chessboard[chess_index[1]][chess_index[0]] = self.chess

        if self.turnChessColor=="black":
            self.turnChessColor="white"
        else:
            self.turnChessColor="black"

        self.lbl = None
        result = self.isWin(self.chess)
        if result != None:
            print(result + '赢了')
            self.showResult(result)
            
        #自动落子
        #self.autoDown()
       


    #坐标转换
    def reversePos(self, a0: QtCore.QPoint):
        if a0.x() <= 50 - 15 or a0.x() >= 590 +15 or a0.y() <= 50 - 15 or a0.y() >= 590+15 :
            return None, None

        self.x = (a0.x()-35)//30
        self.y = (a0.y()-35)//30

        x = 50+30*self.x
        y = 50+30*self.y
        return QPoint(x, y),(self.x, self.y)






    
    def isWin(self,chessman):
        print("in iswin,lastChessman:",chessman.color,chessman.x,chessman.y)
        #水平方向y相同，chessboard[chessman.y][i]
        count = 1
        #左边
        i = chessman.x - 1
        while i>=0:
            if self.chessboard[chessman.y][i] == None or self.chessboard[chessman.y][i].color != chessman.color:
                break
            count += 1
            i -= 1
        #右边
        i = chessman.x + 1
        while i<=18:
            if self.chessboard[chessman.y][i] == None or self.chessboard[chessman.y][i].color != chessman.color:
                break
            count += 1
            i += 1

        if count >=5:
            return chessman.color

        count = 1
        j = chessman.y - 1
        while j >= 0:
            if self.chessboard[j][chessman.x] == None or self.chessboard[j][chessman.x].color != chessman.color:
                break
            count += 1
            j -= 1

        j = chessman.y + 1
        while j <= 18:
            if self.chessboard[j][chessman.x] == None or self.chessboard[j][chessman.x].color != chessman.color:
                break
            count += 1
            j += 1



        if count >=5:
            return chessman.color

        count = 1
        j,i = chessman.y - 1,chessman.x + 1
        while j >= 0 and i <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i].color != chessman.color:
                break
            count += 1
            j -= 1
            i += 1

        j,i = chessman.y + 1,chessman.x - 1
        while i >= 0 and j <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i].color != chessman.color:
                break
            count += 1
            i -= 1
            j += 1
        if count >=5:
            return chessman.color

        count = 1
        j,i = chessman.y-1,chessman.x-1
        while j>=0 and i>=0:
            if self.chessboard[j][i] == None or self.chessboard[j][i].color != chessman.color:
                break
            count += 1
            j -= 1
            i -= 1

        j,i = chessman.y+1,chessman.x+1
        while j<=18 and i<=18:
            if self.chessboard[j][i] == None or self.chessboard[j][i].color != chessman.color:
                break
            count += 1
            j += 1
            i += 1

        if count >=5:
            return chessman.color

        return None


        



    def showResult(self,isWin = None):
        self.gameStatu = False
        if isWin == "white":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/白棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show()
        elif isWin == "black":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/黑棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show() 
        else:
            return

    def restar(self):
        for i in range(16):
            for j in range(16):
                if self.chessboard[i][j] != None:
                    self.chessboard[i][j].close()
                    self.chessboard[i][j] = None
                    self.focusPoint.close()
                else:
                    pass
        if self.lbl != None:
            self.lbl.close() 

        self.gameStatu = True           

        
        

    def lose(self):
        if self.gameStatu == False:
            return
        if self.turnChessColor == "black":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/白棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show()
        elif self.turnChessColor == "white":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/黑棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show()
        else:
            return

    def huiback(self):
        if self.gameStatu == False:
            return
        m = self.history.pop()
        a = self.history2.pop()
        self.chessboard[m.y][m.x] = None
        m.close()  
        a.close() 
        if self.turnChessColor=="black":
            self.turnChessColor="white"
        else:
            self.turnChessColor="black"
     

if __name__ == "__main__":
    import cgitb
    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = DoublePlayGame()
    m.show()
    sys.exit(a.exec_())
    pass