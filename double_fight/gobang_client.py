# -*- coding: utf-8 -*-
# 客户端1代码
import socket



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
        # 将对方的落子点更新到自己的棋盘上
        t.get_change(t2[0], t2[1])
        t.draw_chess()
        changeid(t)
    else:
        pass


def changeid(t):
    if t.id == 1:
        t.id = 2
    if t.id == 2:
        t.id = 1

def client_init_1():

    # 创建 socket 对象
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取服务器ip地址 应该由界面输入 在这里直接用
    host = input('please input the server IP address : ')
    host = socket.gethostname()
    # 设置端口号
    port = 9999
    # 连接服务，指定主机和端口
    c.connect((host, port))


while True:
    client_handle(c, t)
