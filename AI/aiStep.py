# from search import *
from module.search import *
import numpy as np


def getScore(state, pos, key):
    attack = 501 * live4(state, pos, key) + 31 * chong4(state, pos, key) + 31 * live3(state, pos, key) + 11 * mian3(
        state, pos, key) + 51 * live2(state, pos, key)
    key = -key
    defend = 500 * live4(state, pos, key) + 30 * chong4(state, pos, key) + 30 * live3(state, pos, key) + 10 * mian3(
        state, pos, key) + 501 * live2(state, pos, key)
    return attack + defend


def aiStep(state):
    """
    state: (15, 15) 棋盘状态，1、-1分别为双方，0为空，-1表示电脑
    return: array([x, y])表示落子坐标
    """
    key = -1

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
    for opt in opt_list:  # 对每个可选位置打分
        score_list.append(getScore(state, opt, key))

    max_index = score_list.index(max(score_list))

    return opt_list[max_index]


if __name__ == '__main__':
    board = np.zeros((15, 15))
    board[3, 3] = 1
    res = aiStep(board)
    print(res)