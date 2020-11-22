#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    双人对战GUI设计
'''
import sys
import time
import os
sys.path.append('D:/Git/PY_gobang/GUI')
sys.path.append('D:/Git/PY_gobang/GUI/source')
sys.path.append('D:/Git/PY_gobang/AI')
from chessboard import ChessBoard
from gobangGUI import GoBang
import numpy as np
# 客户端1代码
import socket
import threading
import cgitb
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
sys.path.append("D:/Pyfiles/PY_gobang/AI")
sys.path.append('D:/Git/PY_gobang/GUI/double_play')
import MyButton
import gobangGUI
import doublePlayerGUI

recent_place = []
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

# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------

class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)


    def enterEvent(self, e):
        e.ignore()


class Player2GoBang(GoBang):
    backSignal = QtCore.pyqtSignal()  # 返回信号，用来和主界面连接
    def __init__(self):
        super().__init__()
        self.initUI()
        self.c = self.init_clent()
        self.huiqi_flag = True

    def init_clent(self): # 客户端初始化
        # 创建 socket 对象
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取服务器ip地址 应该由界面输入 在这里直接用主机地址代替
        # host = input('please input the server IP address : ')

        host = socket.gethostname()
        # 设置端口号
        port = 9999
        # 连接服务，指定主机和端口

        while True:
            time.sleep(0.5)
            try:
                res = c.connect((host, port))
                if not res:
                    print("connect server", res)
                    break
            except:
                print('等待联机')
        t1 = threading.Thread(target=self.client_recv)
        t1.start()
        return c

    def data_checkout(self, data):
        print('接收数据 : ')
        print(data)
        if data == 'r':
            self.gameover(WHITE)
        if data == 'c':
            # 执行重开函数
            self.piece_now = BLACK
            self.step = 0
            for piece in self.pieces:
                piece.clear()
            self.chessboard.reset()
            self.update()
            return False
        if data == 'h':
            if self.piece_now == BLACK:  # 要连续撤销两次

                self.pieces[self.step - 1].setVisible(False)
                self.pieces[self.step - 2].setVisible(False)
                self.step -= 2
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
            else:  # 要撤销一次

                self.pieces[self.step - 1].setVisible(False)
                self.step -= 1
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
            return False
        return True

    def client_recv(self):
        '''接收数据'''
        while True:
            try:
                data = self.c.recv(1024).decode()
                if self.data_checkout(data):
                    str_list = data.split(' ')
                    x, y = int(str_list[0]), int(str_list[1])
                    self.piece_now = int(str_list[2])
                    self.draw(x, y)
                    recent_place.append([x, y, BLACK])
                    self.ai_down = True  # 解锁 允许鼠标点击下棋
            except:
                pass

    def mousePressEvent(self, e):  # 玩家2下棋

        if e.button() == Qt.LeftButton and self.ai_down:
            x, y = e.x(), e.y()  # 鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)  # 对应棋盘坐标
            if not i is None and not j is None:  # 棋子落在棋盘上，排除边缘
                if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY:  # 棋子落在空白处
                    t1 = (str(i), ' ', str(j), ' ', str(self.piece_now))
                    t2 = ''.join(t1)
                    # 发送棋子坐标到服务器
                    self.c.send(t2.encode('utf-8'))
                    self.draw(i, j)
                    recent_place.append([i, j, WHITE])
                    self.ai_down = False # 加锁 避免鼠标再点击

    # 落子代码
    def draw(self, i, j):
        print('绘图:')
        print(i, j)
        print('self.step')
        print(self.step)
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

    # 认输功能键，不知道为什么卡的厉害。人机对战的认输还没写
    def lose(self):
        self.c.send('r'.encode())
        self.gameover(WHITE)
        self.backSignal.emit()

        self.close()


    # 重开
    def restart(self):
        self.huiqi_flag = True
        self.piece_now = BLACK
        self.step = 0
        for piece in self.pieces:
            piece.clear()
        self.chessboard.reset()
        self.update()
        self.c.send('c'.encode())

    def returnOneStep(self):
        if self.huiqi_flag:
            if self.piece_now == WHITE:  # 要连续撤销两次
                self.pieces[self.step - 1].setVisible(False)
                self.pieces[self.step - 2].setVisible(False)

                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                self.c.send('h'.encode())  # 发送悔棋指令
                self.huiqi_flag = False
                self.piece_now = WHITE
                self.step -= 2
                print('悔棋成功')
            else: # 要撤销一次
                self.pieces[self.step - 1].setVisible(False)
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                self.c.send('h'.encode())  # 发送悔棋指令
                self.huiqi_flag = False
                self.ai_down = True
                self.piece_now = WHITE
                self.step -= 1
                print('悔棋成功')
        else:
            print('悔棋次数已用完！悔棋失败！')
        return

class Mainwindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(760, 650)
        self.setWindowTitle("gobang")
        # 设置窗口图标
        self.setWindowIcon(QIcon("source/icon.ico"))

        # 设置背景图片
        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage("source/gobang_background.png"))
        p.setBrush(QPalette.Background, brush)  # 设置调色版
        self.setPalette(p)  # 给窗口设置调色板

        self.singlePlayerBtn = MyButton.MyButton('source/人机对战_hover.png',
                                                 'source/人机对战_normal.png',
                                                 'source/人机对战_press.png',
                                                 parent=self)
        self.singlePlayerBtn.move(250, 450)

        self.doublePlayerBtn = MyButton.MyButton('source/双人对战_hover.png',
                                                 'source/双人对战_normal.png',
                                                 'source/双人对战_press.png',
                                                 parent=self)
        self.doublePlayerBtn.move(250, 500)

        # 绑定开始双人游戏信号和槽函数
        self.doublePlayerBtn.clicked.connect(self.startDoubleGame)
        self.singlePlayerBtn.clicked.connect(self.startSingleGame)

    def startDoubleGame(self):
        # 构建双人对战界面
        self.doublePlayerGame = Player2GoBang()
        # 绑定返回界面
        self.doublePlayerGame.backSignal.connect(self.showStartGame)

        self.doublePlayerGame.show()  # 显示游戏界面
        self.close()

    def startSingleGame(self):
        self.SingleGame = gobangGUI.GoBang()
        # self.SingleGame = SinglePlayerGame.SinglePlayerGame()
        self.SingleGame.backSignal.connect(self.showStartGame2)
        self.SingleGame.show()
        self.close()

    # 显示开始界面
    def showStartGame(self):
        self.show()
        self.doublePlayerGame.close()

    def showStartGame2(self):
        self.show()
        self.SingleGame.close()

if __name__ == '__main__':
    '''
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())
    '''

    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = Mainwindow()
    m.show()
    sys.exit(a.exec_())