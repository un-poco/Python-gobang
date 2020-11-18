import os
import time
import numpy as np
import sys
sys.path.append('../AI')
# from ai import AI1Step
from utils.ai import AI1Step
"""
使用方法说明：
首先将Gomoku实例化
轮到电脑下棋则：调用：ai_play_1step(self, state)函数
输入：state为当前棋盘的状态状态
输出：落子的坐标
"""
class Gomoku:

    def __init__(self):
        self.state = np.zeros((15,15)) # 当前的棋盘
        self.cur_step = 1  # 步数
        self.max_search_steps = 3  # 最远搜索2回合之后


    def game_result(self):
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(11):
            for y in range(15):
                if self.state[x][y] == 1 and self.state[x + 1][y] == 1 and self.state[x + 2][y] == 1 and self.state[x + 3][y] == 1 and self.state[x + 4][y] == 1:
                    return 1
                if self.state[x][y] == 2 and self.state[x + 1][y] == 2 and self.state[x + 2][y] == 2 and self.state[x + 3][y] == 2 and self.state[x + 4][y] == 2:
                    return 2

        # 2. 判断是否纵向连续五子
        for x in range(15):
            for y in range(11):
                if self.state[x][y] == 1 and self.state[x][y + 1] == 1 and self.state[x][y + 2] == 1 and self.state[x][y + 3] == 1 and self.state[x][y + 4] == 1:
                    return 1
                if self.state[x][y] == 2 and self.state[x][y + 1] == 2 and self.state[x][y + 2] == 2 and self.state[x][y + 3] == 2 and self.state[x][y + 4] == 2:
                    return 2

        # 3. 判断是否有左上-右下的连续五子
        for x in range(11):
            for y in range(11):
                if self.state[x][y] == 1 and self.state[x + 1][y + 1] == 1 and self.state[x + 2][y + 2] == 1 and self.state[x + 3][y + 3] == 1 and self.state[x + 4][y + 4] == 1:
                    return 1
                if self.state[x][y] == 2 and self.state[x + 1][y + 1] == 2 and self.state[x + 2][y + 2] == 2 and self.state[x + 3][y + 3] == 2 and self.state[x + 4][y + 4] == 2:
                    return 2


        # 4. 判断是否有右上-左下的连续五子
        for x in range(11):
            for y in range(11):
                if self.state[x + 4][y] == 1 and self.state[x + 3][y + 1] == 1 and self.state[x + 2][y + 2] == 1 and self.state[x + 1][y + 3] == 1 and self.state[x][y + 4] == 1:
                    return 1
                if self.state[x + 4][y] == 2 and self.state[x + 3][y + 1] == 2 and self.state[x + 2][y + 2] == 2 and self.state[x + 1][y + 3] == 2 and self.state[x][y + 4] == 2:
                    return 2


    def ai_play_1step_py_python(self):
        ai1 = AI1Step(self, self.cur_step, True)  # AI判断下一步执行什么操作
        st = time.time()
        ai1.search(0, [set(), set()], self.max_search_steps)  # 最远看2回合之后
        ed = time.time()
        print('生成了%d个节点，用时%.4f，评价用时%.4f' % (len(ai1.method_tree), ed - st, ai1.t))
        # if ai1.next_node_dx_list[0] == -1:
        #     raise ValueError('ai.next_node_dx_list[0] == -1')
        # print(ai1.method_tree[ai1.next_node_dx_list[0]])
        ai_ope = ai1.method_tree[ai1.next_node_dx_list[0]].ope
        # print(ai_ope)
        # print(ai1.method_tree[ai1.next_node_dx_list[0]].score)
        # if self.state[ai_ope[0]][ai_ope[1]] != 0:
        #     raise ValueError('self.game_map[ai_ope[0]][ai_ope[1]] = %d' % self.state[ai_ope[0]][ai_ope[1]])
        self.cur_step += 2
        # print(self.cur_step)
        # self.state[ai_ope[0]][ai_ope[1]] = 2

        return [ai_ope[0], ai_ope[1]]


    #  电脑做出回应
    def ai_play_1step(self,state):
        self.max_search_steps = 2
        self.state = state
        row, col= self.ai_play_1step_py_python()
        return row,col




