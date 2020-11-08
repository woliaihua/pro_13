from multpro import *
from setup import pool_num
from setup import start_exchange_integral
from tkinter import messagebox
from tkinter import Tk
"""
多进程打开浏览器，刷新页面监测是否有可兑换商品，有就兑换
"""
if __name__ == '__main__':
    freeze_support()
    # with open('账号.txt','r',encoding='utf-8') as f:
    #     txt_lines = f.readlines()
    # start_accept_task((9022,txt_lines))
    N = int(pool_num)  # 进程数
    pool = Pool(N)
    with open('账号.txt', 'r', encoding='utf-8') as f:
        txt_lines = f.readlines()
    # 每个进程平均分配账号
    list_args = list(zip(range(9022, 9022 + N), txt_lines))
    print(list_args)
    pool.map(start_exchange_integral, list_args)
