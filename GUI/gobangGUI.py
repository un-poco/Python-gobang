#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    python course design_Gobang
    GUI part designed by Adrian
    using pyQT5
    2020/10/31
'''

from chessboard import ChessBoard
from ai import searcher
import MyButton
import numpy as np

# 棋盘基本参数等
WIDTH = 760
HEIGHT = 650
MARGINXL = 100
MARGINXR = 164
MARGINX = 0.5 * (MARGINXL + MARGINXR)
MARGINY = 77
GRID = (WIDTH - 2 * MARGINX) / (15 - 1)
PIECE = 34
EMPTY = 0
BLACK = 1
WHITE = 2
recent_place = []  # 用于悔棋的栈

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
from PyQt5 import *


# ----------------------------------------------------------------------
# 定义线程类执行AI的算法,这里我嫖的一个csdn的AI算法，麻烦负责相关算法的同学对接一下
# ----------------------------------------------------------------------
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)

    # 构造函数里增加形参
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board

    # 重写 run() 函数
    def run(self):
        self.ai = searcher()
        self.ai.board = self.board
        x, y = self.ai.search(2, 2)
        recent_place.append([x, y, WHITE])
        self.finishSignal.emit(x, y)


# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()


class GoBang(QWidget):
    backSignal = QtCore.pyqtSignal()  # 返回信号，用来和主界面连接

    def __init__(self):
        super().__init__()
        self.initUI()
        self.huiqi_flag = 1

    def initUI(self):  # UI初始化

        self.chessboard = ChessBoard()  # 棋盘类，详见chessboard.py

        palette1 = QPalette()  # 设置棋盘背景
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('source/游戏界面1.png')))
        self.setPalette(palette1)

        # self.setCursor(Qt.PointingHandCursor)  # 鼠标变成手指形状
        self.sound_piece = QSound("sound/move.wav")  # 加载落子音效
        self.sound_win = QSound("sound/win.wav")  # 加载胜利音效
        self.sound_defeated = QSound("sound/defeated.wav")  # 加载失败音效

        self.resize(WIDTH, HEIGHT)  # 画布大小，设为固定值，不允许缩放
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        self.setWindowTitle("GoBang")  # 窗口名称
        self.setWindowIcon(QIcon('source/icon.ico'))  # 窗口图标

        # 所有按钮的图标和布局
        self.backBtn = MyButton.MyButton('source/返回按钮_hover.png',
                                         'source/返回按钮_normal.png',
                                         'source/返回按钮_press.png',
                                         parent=self)
        self.backBtn.move(610, 80)

        self.startBtn = MyButton.MyButton('source/开始按钮_hover.png',
                                          'source/开始按钮_normal.png',
                                          'source/开始按钮_press.png',
                                          parent=self)
        self.startBtn.move(610, 180)

        self.returnBtn = MyButton.MyButton('source/悔棋按钮_hover.png',
                                           'source/悔棋按钮_normal.png',
                                           'source/悔棋按钮_press.png',
                                           parent=self)
        self.returnBtn.move(610, 400)

        self.loseBtn = MyButton.MyButton('source/认输按钮_hover.png',
                                         'source/认输按钮_normal.png',
                                         'source/认输按钮_press.png',
                                         parent=self)
        self.loseBtn.move(610, 500)

        # 绑定按钮
        self.backBtn.clicked.connect(self.goBack)
        self.startBtn.clicked.connect(self.restart)
        self.loseBtn.clicked.connect(self.lose)
        self.returnBtn.clicked.connect(self.returnOneStep)

        # self.gameStatu = []

        self.black = QPixmap('source/black.png')  # 黑白棋子
        self.white = QPixmap('source/white.png')

        self.piece_now = BLACK  # 黑棋先行
        self.my_turn = True  # 玩家先行
        self.step = 0  # 步数
        self.x, self.y = 1000, 1000

        # self.mouse_point.setGeometry(270, 270, PIECE, PIECE)
        self.pieces = [LaBel(self) for i in range(225)]  # 新建棋子标签，准备在棋盘上绘制棋子
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变

        self.ai_down = True  # AI已下棋，主要是为了加锁，当值是False的时候说明AI正在思考，这时候玩家鼠标点击失效，要忽略掉 mousePressEvent

        self.setMouseTracking(True)
        self.show()

    # 返回键设计，回到主菜单
    def goBack(self):
        self.backSignal.emit()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.backSignal.emit()

    def paintEvent(self, event):  # 画出指示箭头
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    # def mouseMoveEvent(self, e):  # 黑色棋子随鼠标移动
    #     # self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
    #     self.mouse_point.move(e.x() - 16, e.y() - 16)

    def mousePressEvent(self, e):  # 玩家下棋
        if e.button() == Qt.LeftButton and self.ai_down == True:
            x, y = e.x(), e.y()  # 鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)  # 对应棋盘坐标
            if not i is None and not j is None:  # 棋子落在棋盘上，排除边缘
                if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY:  # 棋子落在空白处
                    self.draw(i, j)  # 玩家棋子绘制
                    recent_place.append([i, j, BLACK])

                    # ----------------------------------------------------------------------
                    # 这里要对接双人落子，我准备偷个懒，直接把ui的全部代码粘到另一个文件里，修改落子代码实现双人对战。对接的同学有好的传参方式也可以直接修改这份代码。
                    # ----------------------------------------------------------------------

                    self.ai_down = False
                    board = self.chessboard.board()
                    self.AI = AI(board)  # 新建线程对象，传入棋盘参数
                    self.AI.finishSignal.connect(self.AI_draw)  # 结束线程，传出参数
                    self.AI.start()  # run

    # ----------------------------------------------------------------------

    # 以下部分和AI落子相关，对接的同学请注意
    # ----------------------------------------------------------------------

    def AI_draw(self, i, j):
        if self.step != 0:
            self.draw(i, j)  # AI
            self.x, self.y = self.coordinate_transform_map2pixel(i, j)
        self.ai_down = True
        self.update()

    def drawLines(self, qp):  # 指示AI当前下的棋子
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

    # 落子代码
    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if self.piece_now == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # 放置黑色棋子
            self.pieces[self.step].setVisible(True)
            self.piece_now = WHITE
            self.chessboard.draw_xy(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # 放置白色棋子
            self.pieces[self.step].setVisible(True)
            self.piece_now = BLACK
            self.chessboard.draw_xy(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # 画出棋子
        self.sound_piece.play()  # 落子音效
        self.step += 1  # 步数+1

        winner = self.chessboard.anyone_win(i, j)  # 判断输赢
        if winner != EMPTY:
            # self.mouse_point.clear()
            self.gameover(winner)

    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return MARGINXL + j * GRID - PIECE / 2, MARGINY + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGINY) / GRID)), int(round((x - MARGINXL) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            return None, None
        else:
            return i, j

    # 这块代码后期还可以再改，用图片做出来应该会更好看
    def gameover(self, winner):
        if winner == BLACK:
            self.sound_win.play()
            reply = QMessageBox.question(self, 'You Win!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            self.sound_defeated.play()
            reply = QMessageBox.question(self, 'You Lost!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:  # 复位
            self.piece_now = BLACK
            # self.mouse_point.setPixmap(self.black)
            self.step = 0
            for piece in self.pieces:
                piece.clear()
            self.chessboard.reset()
            self.update()
        else:
            self.close()

    # 认输功能键
    def lose(self):
        # if self.gameStatu == False:
        #     return
        if self.piece_now == BLACK:
            self.gameover(WHITE)
        # elif self.turnChessColor == "white":
        #     self.lbl = QLabel(self)
        #     self.lbl.setPixmap(QPixmap("source/黑棋胜利.png"))
        #     self.lbl.move(150,150)
        #     self.lbl.show()
        else:
            return

    # 重开
    def restart(self):
        self.piece_now = BLACK
        self.huiqi_flag = 1
        self.step = 0
        for piece in self.pieces:
            piece.clear()
        self.chessboard.reset()
        self.update()

    # 这个理论上要做悔棋功能，看看写代码的同学是怎么实现的。
    def returnOneStep(self):
        if self.huiqi_flag:

            # AI的下棋速度很快 默认每次悔棋的时候都是悔去AI的棋子和自己的棋子 所有等到AI下完之后再悔棋

            self.pieces[self.step - 1].setVisible(False)
            self.pieces[self.step - 2].setVisible(False)

            current_place = recent_place.pop()
            self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
            current_place = recent_place.pop()
            self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
            self.pieces[self.step]
            self.huiqi_flag = 0
            print('悔棋成功')
        else:
            print('悔棋次数已用完，悔棋失败')
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())
