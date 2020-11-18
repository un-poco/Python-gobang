import os
import numpy as np
# 五子棋类
class chessboard(object):
    #初始化棋盘
    def __init__(self, color):
        self.size = 15
        #初始化棋盘  15 15的一个数组 0代表未填 1代表黑 -1代表白 先全部初始化为0
        self.board = np.zeros((15, 15))
        # 棋子的颜色 0代表未填 1代表黑 -1代表白
        self.color = color
    # id 辅助变量 0代表初始化 1代表轮到我方回合 2代表轮到对方回合
    id = 0

    # 判断胜利条件的函数 还未添加
    def is_end(self):
        return False


    # 由GUI界面点击发生状态改变 更改棋盘的状态
    def get_change(self,x, y):
        self.board[x][y] = self.color

    # 绘制棋盘 由pyqt实现 还未添加
    def draw_chess(self):
        print("draw chess")

