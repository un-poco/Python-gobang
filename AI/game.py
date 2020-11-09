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
getresult函数还需要交流一下，因为评估分数会用到
"""
class Gomoku:

    def __init__(self):
        self.state = np.zeros((15, 15))  # 当前的棋盘
        self.cur_step = 0  # 步数
        self.max_search_steps = 3  # 最远搜索2回合之后


    def game_result(self, show=False):
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""


    def ai_play_1step_py_python(self):
        ai1 = AI1Step(self, self.cur_step, True)  # AI判断下一步执行什么操作
        st = time.time()
        ai1.search(0, [set(), set()], self.max_search_steps)  # 最远看2回合之后
        ed = time.time()
        print('生成了%d个节点，用时%.4f，评价用时%.4f' % (len(ai1.method_tree), ed - st, ai1.t))
        if ai1.next_node_dx_list[0] == -1:
            raise ValueError('ai.next_node_dx_list[0] == -1')
        ai_ope = ai1.method_tree[ai1.next_node_dx_list[0]].ope
        if self.state[ai_ope[0]][ai_ope[1]] != 0:
            raise ValueError('self.game_map[ai_ope[0]][ai_ope[1]] = %d' % self.state[ai_ope[0]][ai_ope[1]])
        self.cur_step += 1
        self.state[ai_ope[0]][ai_ope[1]] = -1
        return [ai_ope[0], ai_ope[1]]


    #  电脑做出回应
    def ai_play_1step(self, state):
        self.max_search_steps = 2
        self.state = state
        self.ai_play_1step_py_python()