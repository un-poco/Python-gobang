# -*- coding: utf-8 -*-
# 客户端代码
import socket
from gobang_chessboard import chessboard

black = 1
white = -1


def client_handle(c, t):
    if t.id == 1:
        # 得到落子点 应该由GUI界面输入 这里由命令行输入
        x = int(input("please input x"))
        y = int(input("please input y"))
        t.get_change(x, y)
        # 将坐标转换为字符串 便于通过TCP输出
        t1 = (str(x), str(y))
        t2 = ''.join(t1)
        print(t2)
        c.send(t2.encode('utf-8'))
        print('__________________wait__________________')
        # 接收到应答信号 说明坐标已经发给服务端
        ans = c.recv(1024).decode('utf-8')
        print(ans)
        # 绘制新的棋盘
        t.draw_chess()
        # 状态改变
        changeid(t)
    elif t.id == 2:
        # 对方落子 己方等待和对方同步
        ans = c.recv(1024).decode('utf-8')
        print(ans)
        t1 = list(ans)
        t2 = [int(x) for x in t1]
        t.get_change(t2[0], t2[1])
        changeid(t)
    else:
        pass


def changeid(t):
    if t.id == 1:
        t.id = 2
    if t.id == 2:
        t.id = 1


# pyqt界面按下双人对战按钮 跳转到双人对战界面 按下发起对战按钮 弹出输入服务器ip地址窗口

# 创建一个棋盘对象 同时初始化该客户端棋子颜色 由GUI界面输入 这里直接选择
# 客户端2选择白色
t = chessboard(color=white)
# 黑先
t.id = 2

# 创建 socket 对象
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取服务器ip地址 应该由界面输入 在这里直接用
host = socket.gethostname()
# 设置端口号
port = 9999
# 连接服务，指定主机和端口
c.connect((host, port))
while True:
    client_handle(c, t)
