import sys
sys.path.append('../AI')
from search import *

import numpy as np


def getScore(state, pos):
    key = 2
    attack = 100000 * finish5(state, pos, key) + 1001 * live4(state, pos, key) + 301 * chong4(state, pos, key) + \
             301 * live3(state, pos, key) + 101 * mian3(state, pos, key) + 51 * live2(state, pos, key)
    key = 1
    defend = 10000 * finish5(state, pos, key) + 1000 * live4(state, pos, key) + 300 * chong4(state, pos, key) + \
             300 * live3(state, pos, key) + 100 * mian3(state, pos, key) + 50 * live2(state, pos, key)
    return attack + defend


def aiStep(state):
    """
    state: (15, 15) 棋盘状态，1、-1分别为双方，0为空，-1表示电脑
    return: array([x, y])表示落子坐标
    """

    opt_list = np.where(state == 0)  # 落子条件一：这个格子必须为空
    opt_list = [np.array([opt_list[0][i], opt_list[1][i]]) for i in range(len(opt_list[0]))]  # 每个坐标转换成ndarray

    de_indx = []
    for i in range(len(opt_list)):  # 落子条件二：周围8格内必须有至少一个棋子
        loc = opt_list[i]
        flag = False
        for j in range(len(dx)):
            indx = np.array(loc + (dx[j], dy[j]))
            if (indx > 14).any() or (indx < 0).any():
                continue
            if state[tuple(indx)] != 0:
                flag = True
                break
        if not flag:
            de_indx.append(i)
    d = 0
    for e in de_indx:
        e -= d
        _ = opt_list.pop(e)
        d += 1

    score_list = []
    for i in range(len(opt_list)):  # 对每个可选位置打分
        opt = opt_list[i]
        score_list.append(getScore(state, opt))

    max_index = score_list.index(max(score_list))
    return opt_list[max_index]


if __name__ == '__main__':
    board = np.zeros((15, 15))
    board[3, 3] = 1
    res = live2(board, np.array([2, 2]), 1)
    print(res)
