from multpro import *
from setup import start_accept_task
from tkinter import messagebox
from tkinter import Tk
"""
多进程打开浏览器接取任务
"""
if __name__ == '__main__':

    # with open('账号.txt','r',encoding='utf-8') as f:
    #     txt_lines = f.readlines()
    # start_accept_task((9022,txt_lines))
    freeze_support()
    N = 2  # 进程数
    pool = Pool(N)
    with open('账号.txt', 'r', encoding='utf-8') as f:
        txt_lines = f.readlines()
    # 每个进程平均分配账号
    shang, yu = divmod(len(txt_lines), N)
    l = []
    for lines in grouper(txt_lines, shang + 1):
        l.append(lines)
    list_args = list(zip(range(9022, 9022 + N), l))
    pool.map(start_accept_task, list_args)
    root = Tk()
    root.withdraw()
    a = messagebox.showwarning('提示', '任务领取全部完成！')
    root.quit()
    root.destroy()  # 销毁部件
