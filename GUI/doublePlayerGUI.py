#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    双人对战GUI设计
'''
import sys
import os

sys.path.append('D:/Git/PY_gobang/GUI')
sys.path.append('D:/Git/PY_gobang/GUI/source')
sys.path.append('D:/Git/PY_gobang/AI')
from chessboard import ChessBoard
import MyButton

import numpy as np
# 客户端1代码
import socket
import threading

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

sys.path.append(r'D:\Git\PY_gobang\GUI\double_play')
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter

from PyQt5.QtMultimedia import QSound


def server():
    # 执行我自己目录下的服务器
    os.system('python double_play/gobang_server.py')


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
        threading.Thread(target=server).start()
        self.c = self.init_clent()
        self.huiqi_flag = True

    def init_clent(self):  # 客户端初始化
        # 创建 socket 对象
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取服务器ip地址 应该由界面输入 在这里直接用主机地址代替
        # host = input('please input the server IP address : ')
        host = socket.gethostname()
        # 设置端口号
        port = 9999
        # 连接服务，指定主机和端口
        c.connect((host, port))
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
            if self.piece_now == WHITE:  # 要连续撤销两次
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
                    recent_place.append([x, y, WHITE])

                    self.ai_down = True  # 解锁 允许鼠标点击下棋
            except:
                pass

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

        self.setWindowTitle("GoBang_BLACK")  # 窗口名称
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

        self.step = 0  # 步数
        self.x, self.y = 1000, 1000

        self.pieces = [LaBel(self) for i in range(225)]  # 新建棋子标签，准备在棋盘上绘制棋子
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变

        # self.mouse_point.raise_()  # 鼠标始终在最上层
        self.ai_down = True  # 主要是为了加锁，当值是False的时候在等待对方下棋，这时候己方鼠标点击失效，要忽略掉 mousePressEvent

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

    def mousePressEvent(self, e):  # 玩家1下棋

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
                    recent_place.append([i, j, BLACK])
                    self.ai_down = False  # 加锁 避免鼠标再点击

    def drawLines(self, qp):  # 绘制lines
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

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

    # 认输功能键，不知道为什么卡的厉害。人机对战的认输还没写
    def lose(self):
        self.c.send('r'.encode())
        self.gameover(WHITE)
        self.backSignal.emit()

        self.close()

    # 重开，这个问题有点大，重新绘图我没实现。目前是把数组清空了，图没变(在上面重新画棋盘也太蠢了吧，刷新界面会比较好但是我没写出来:/)
    def restart(self):
        self.huiqi_flag = True
        self.piece_now = BLACK
        self.step = 0
        for piece in self.pieces:
            piece.clear()
        self.chessboard.reset()
        self.update()
        self.c.send('c'.encode())

    # 这个理论上要做悔棋功能，看看写代码的同学是怎么实现的。
    def returnOneStep(self):
        if self.huiqi_flag:
            if self.piece_now == BLACK:  # 要连续撤销两次
                self.pieces[self.step - 1].setVisible(False)
                self.pieces[self.step - 2].setVisible(False)

                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                self.c.send('h'.encode())  # 发送悔棋指令
                self.huiqi_flag = False
                self.piece_now = BLACK
                self.step -= 2
                print('悔棋成功')
            else: # 要撤销一次
                self.pieces[self.step - 1].setVisible(False)
                current_place = recent_place.pop()
                self.chessboard.draw_xy(current_place[0], current_place[1], 0)  # 清空对应棋子
                self.c.send('h'.encode())  # 发送悔棋指令
                self.huiqi_flag = False
                self.ai_down = True
                self.piece_now = BLACK
                self.step -= 1
                print('悔棋成功')
        else:
            print('悔棋次数已用完！悔棋失败！')
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())
