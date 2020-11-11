#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from  time import sleep
import random
import json
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
        s4 = self.s.post(url,data=data,headers=header)
        response = s4.text#响应正文
        return response

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
        res = self.send_post(url, data, header)
        return json.loads(res)


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

    def duihuan_300(self):
        """
        兑换300的积分卡
        :return:
        """
        url = 'http://yqdz.meiri100.cn/Mall/order_add'
        header = {
                  "Host": "yqdz.meiri100.cn",
                  # "Cookie":get_strCookie(),
                  "Referer": "http://yqdz.meiri100.cn/mall/cart_info",
                  "X-Requested-With": "XMLHttpRequest"
                  }
        data = {
            "auto_ids": "170,1,300元京东卡,30000,http://files.mangsou.com/public/zbline/upfile/2020/11/10/5faa46e93809c767102702.png,3",
            "addr": '',
            "consigneePhone": '',
            "consigneeName": '',
            "money": 30000,
        }
        res = self.s.get(url, params=data, headers=header)
        return res.text

    def get_content(self):
        """"""
        pass
if __name__ == '__main__':
    response_ = [{'goods_status': 1, 'goods_name': '100元京东卡',
                  'original_img': 'http://files.mangsou.com/public/zbline/upfile/2020/11/10/5faa5f12967dc037293438.png',
                  'goods_url': '', 'sale_num': 1000, 'goods_price': 10000, 'num': 1000, 'inventory': 0,
                  'goods_detail': '', 'goods_number': '', 'group_id': '7b08022526618cf1eab62a8f81c6c437', 'is_ture': 3,
                  'goods_thumb': '', 'id': 176, 'order_num': 0, 'goods_img': '', 'goods_code': ''},
                 {'goods_status': 1, 'goods_name': '20元京东卡',
                  'original_img': 'http://files.mangsou.com/public/zbline/upfile/2020/11/10/5faa5bcdd2c73246692300.png',
                  'goods_url': '', 'sale_num': 2500, 'goods_price': 2000, 'num': 2500, 'inventory': 0,
                  'goods_detail': '', 'goods_number': '', 'group_id': '7b08022526618cf1eab62a8f81c6c437', 'is_ture': 3,
                  'goods_thumb': '', 'id': 175, 'order_num': 0, 'goods_img': '', 'goods_code': ''},
                 {'goods_status': 1, 'goods_name': '50元京东卡',
                  'original_img': 'http://files.mangsou.com/public/zbline/upfile/2020/11/10/5faa5ba986423905189189.png',
                  'goods_url': '', 'sale_num': 1000, 'goods_price': 5000, 'num': 1000, 'inventory': 0,
                  'goods_detail': '', 'goods_number': '', 'group_id': '7b08022526618cf1eab62a8f81c6c437', 'is_ture': 3,
                  'goods_thumb': '', 'id': 174, 'order_num': 0, 'goods_img': '', 'goods_code': ''},
                 {'goods_status': 1, 'goods_name': '300元京东卡',
                  'original_img': 'http://files.mangsou.com/public/zbline/upfile/2020/11/10/5faa46e93809c767102702.png',
                  'goods_url': '', 'sale_num': 1896, 'goods_price': 30000, 'num': 2000, 'inventory': 104,
                  'goods_detail': '', 'goods_number': '', 'group_id': '7b08022526618cf1eab62a8f81c6c437', 'is_ture': 3,
                  'goods_thumb': '', 'id': 170, 'order_num': 0, 'goods_img': '', 'goods_code': ''}]
    S = SendRequest()
    S.login('16733815003', '123456')
    while True:
        sleep(random.uniform(0.5,1.5))
        res = S.get_goods_list()
        print('商品发放监测中...')
        if res:
            print('商品发放成功，开始抢购')
            break
    #获取当前账号积分
    integral = S.get_integral()  # 获取积分
    l2 = [('300元京东卡', 30000), ('100元京东卡', 10000), ('50元京东卡', 5000), ('20元京东卡', 2000)]
    l = get_suds2(integral, l2)  # 获取可以购买的商品与个数 [('300元京东卡', 1, 30000), ('100元京东卡', 1, 10000)]
    for index, (name, goods_num, base_integral) in enumerate(l):
        for dic in response_:

