# -*- coding: utf-8 -*-
# 服务器端 首先运行这个程序 建立服务器 后期有需要可以使用云服务器
import os
import socket
import json
import threading
import time
import sys
from gobang_chessboard import chessboard
from queue import Queue


def server_handle_1(c1, c2):
    # 接受到client1的消息 发送到client2上去
    while True:
        data = c1.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        c2.send(('%s' % data.decode('utf-8')).encode('utf-8'))

def server_handle_2(c1, c2):
    # 接受到client1的消息 发送到client2上去
    while True:
        data = c2.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        c1.send(('%s' % data.decode('utf-8')).encode('utf-8'))


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
port = 9999
# 绑定端口号
s.bind((host, port))
address = (host, port)
# 设置最大连接数，超过后排队
s.listen(2)


c1, addr1 = s.accept()
print(c1, addr1)  # 打印接受到的信息

c2, addr2 = s.accept()
print(c2, addr2)  # 打印接受到的信息
t1 = threading.Thread(target=server_handle_1, args=(c1, c2))
t2 = threading.Thread(target=server_handle_2, args=(c1, c2))
t1.start()
t2.start()
while 1:
   pass

s.close()
