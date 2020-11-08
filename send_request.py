#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from  time import sleep
from tkinter import messagebox
from tkinter import Tk
import re
from locale import atof, setlocale, LC_NUMERIC
from jifen_2_goods import get_suds2
import re
import datetime
setlocale(LC_NUMERIC, 'English_US')


class SendRequest():
    def __init__(self):
        self.s = requests.session()

    def login(self,u='16531009626',p='123456'):
        data ={'username':u,
               'password':p}
        headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                  "Content-Type":'application/x-www-form-urlencoded; charset=UTF-8',
                  "Referer": "http://yqdz.meiri100.cn/login/index?group_id=7b08022526618cf1eab62a8f81c6c437"}

        url = 'http://yqdz.meiri100.cn/login/login_ok'
        self.s.post(url=url,data=data,headers=headers)

    def get_strCookie(self):
        data ={'username':'16531009626',
               'password':'123456'}
        headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                  "Content-Type":'application/x-www-form-urlencoded; charset=UTF-8',
                  "Referer": "http://yqdz.meiri100.cn/login/index?group_id=7b08022526618cf1eab62a8f81c6c437"}

        url = 'http://yqdz.meiri100.cn/login/login_ok'
        self.s.post(url=url,data=data,headers=headers)
        str_cookie = ''
        for k,v  in self.s.cookies.iteritems():
            str_cookie = str_cookie +k+ '=%s' % v
        return str_cookie

    def send_post(self,url,data,header):
        L= [] #用来收集请求结果
        s4 = self.s.post(url,data=data,headers=header)
        response = s4.text#响应正文
        L.append(response)
        return L

    def send_get(self,url,header):
        L= [] #用来收集请求结果
        s4 = self.s.get(url,headers=header)
        return s4.text


    def get_goods_list(self):
        """
        获取商品列表，看是否有商推出
        :return:
        """
        url = 'http://yqdz.meiri100.cn/Mall/get_goods_list?p=1&psize=10'
        header = {'Origin': 'http://yqdz.meiri100.cn',
                  "Host": "yqdz.meiri100.cn",
                  # "Cookie":get_strCookie(),
                  "Referer": "http://yqdz.meiri100.cn/mall/index",
                  "Content-Type": "text/html; charset=UTF-8"
                  }
        data = {
            "p": 1,
            "psize": 10
        }
        S = SendRequest()
        S.login()
        while True:
            sleep(0.25)
            L = S.send_post(url, data, header)
            print('服务刷新检测是否放法商品')
            if L[0] != '[]':
                print('商品发放成功，开始抢购')
                return True

    def get_integral(self):
        """
        获取积分
        :return:int 积分
        """
        url = 'http://yqdz.meiri100.cn/Mall/cart_info'
        header = {'Origin': 'http://yqdz.meiri100.cn',
                  "Host": "yqdz.meiri100.cn",
                  # "Cookie":get_strCookie(),
                  "Referer": "http://yqdz.meiri100.cn/mall/index",
                  }
        res = S.send_get(url, header)
        integral = re.search('<span class="score">(.+?)</span>', res).group(1)
        try:
            self.integral = int(integral)
        except:
            self.integral = int(atof(integral))
        return self.integral
if __name__ == '__main__':
    url = 'http://yqdz.meiri100.cn/Mall/get_goods_list?p=1&psize=10'
    header = {'Origin':'http://yqdz.meiri100.cn',
              "Host":"yqdz.meiri100.cn",
              #"Cookie":get_strCookie(),
              "Referer": "http://yqdz.meiri100.cn/mall/index",
              "Content-Type": "text/html; charset=UTF-8"
              }
    data = {
        "p":1,
        "psize":10
    }
    S = SendRequest()
    S.login('17042806041','521000')
    print(datetime.datetime.now())
    print(S.get_integral())
    print(datetime.datetime.now())
    # for i in range(50000):
    #     sleep(1)
    #     L = S.send_post(url,data,header)
    #     print(L[0])
    #     if L[0] != '[]':
    #         root = Tk()
    #         root.withdraw()
    #         a = messagebox.showwarning('提示', '发放了')
    #         root.quit()
    #         root.destroy()  # 销毁部件
    #         break