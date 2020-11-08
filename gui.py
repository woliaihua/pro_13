#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
#from printer_pywin32 import PrinterPywin32
from tkinter import ttk


class PrinterTkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title("打印机监控系统")

        self.frame_left_top = Frame(width=400, height=200)
        self.frame_right_top = Frame(width=400, height=200)
        self.frame_center = Frame(width=800, height=400)
        self.frame_bottom = Frame(width=800, height=50)

        # 定义左上方区域
        self.left_top_title = Label(self.frame_left_top, text="打印状态:", font=('Arial', 25))
        self.left_top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=30)

        self.var_success = StringVar()  # 声明成功数
        self.var_false = StringVar()    # 声明失败数

        self.left_top_frame = Frame(self.frame_left_top)
        self.left_top_frame_left1 = Label(self.frame_left_top, text="打印成功数", font=('Arial', 20))
        self.left_top_frame_left2 = Label(self.frame_left_top, textvariable=self.var_success, font=('Arial', 15))
        self.get_success()  # 调用方法更新成功数
        self.left_top_frame_right1 = Label(self.frame_left_top, text="打印失败数", font=('Arial', 20))
        self.left_top_frame_right2 = Label(self.frame_left_top, textvariable=self.var_false, font=('Arial', 15))
        self.get_false()    # 调用方法更新失败数
        self.left_top_frame_left1.grid(row=1, column=0)
        self.left_top_frame_left2.grid(row=1, column=1)
        self.left_top_frame_right1.grid(row=2, column=0)
        self.left_top_frame_right2.grid(row=2, column=1)

        # 定义右上方区域
        self.var_entry = StringVar()

        self.right_top_title = Label(self.frame_right_top, text="重新打印的任务编号：", font=('Arial', 20))
        self.right_top_entry = Entry(self.frame_right_top, textvariable=self.var_entry)

        self.number = int
        self.right_top_button = Button(self.frame_right_top, text="确定", command=self.button_restart, font=('Arial', 15))
        self.right_top_title.grid(row=0, column=0)
        self.right_top_entry.grid(row=1, column=0)
        self.right_top_button.grid(row=2, column=0, padx=20, pady=20)

        # 定义中心列表区域
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=("a", "b", "c", "d", "e"))
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("a", width=50, anchor="center")
        self.tree.column("b", width=200, anchor="center")
        self.tree.column("c", width=200, anchor="center")
        self.tree.column("d", width=100, anchor="center")
        self.tree.column("e", width=150, anchor="center")
        self.tree.heading("a", text="编号")
        self.tree.heading("b", text="打印时间")
        self.tree.heading("c", text="打印名称")
        self.tree.heading("d", text="打印任务编号")
        self.tree.heading("e", text="打印状态")

        # 调用方法获取表格内容插入
        self.get_tree()
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.root.mainloop()

    # 得到打印成功数
    def get_success(self):
        self.var_success.set('1000')
        self.left_top_frame_left2.after(500, self.get_success)

    # 得到打印失败数
    def get_false(self):
        self.var_false.set('10')
        self.left_top_frame.after(500, self.get_false)

    # 表格内容插入
    def get_tree(self):
        # 删除原节点
        for _ in map(self.tree.delete, self.tree.get_children("")):
            pass
        # 更新插入新节点
        for i in range(50):
            self.tree.insert("", "end", values=(i + 1, 666,666,666,666))
        self.tree.after(500, self.get_tree)

    # 重新打印
    def button_restart(self):
        self.number = self.right_top_entry.get()


if __name__ == '__main__':
    PrinterTkinter()