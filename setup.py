import random
from time import sleep
from jifen_2_goods import get_suds2
from send_request import SendRequest
import sys



def goods_duihuan(u, p):
    S1 = SendRequest()
    S1.login(u, p)
    # 获取当前账号积分
    integral = S1.get_integral()  # 获取积分
    print("当前账号{u}剩余积分{integral}".format(u=u, integral=integral))
    l2 = [('300元京东卡', 30000), ('100元京东卡', 10000), ('50元京东卡', 5000), ('20元京东卡', 2000)]
    l = get_suds2(integral, l2)  # 获取可以购买的商品与个数 [('300元京东卡', 1, 30000), ('100元京东卡', 1, 10000)]
    if l:
        response_ = S1.get_goods_list()  # 获取商品
        for index, (goodsname, goods_num, base_integral) in enumerate(l):
            for dic in response_:
                if goodsname == dic.get('goods_name'):
                    if int(dic.get('inventory')) >= goods_num:  # 剩余的卡是不是大于可兑换的数量
                        data = {
                            "auto_ids": "{id},{goods_num},{goods_name},{price},{png_src},3".format(
                                id=dic.get('id'), goods_num=goods_num, goods_name=dic.get('goods_name'),
                                price=dic.get('goods_price'), png_src=dic.get('original_img')),
                            "addr": '',
                            "consigneePhone": '',
                            "consigneeName": '',
                            "money": goods_num * int(dic.get('goods_price')),
                        }
                        res = S1.duihuan(data)
                        if res.get('success') == 1:  # 兑换成功
                            print('{username}兑换成功 {goodsname}{num}个，兑换后积分{integral2}'.format(username=u,
                                                                                             goodsname=goodsname,
                                                                                             num=goods_num,
                                                                                             integral2=integral - goods_num * int(
                                                                                                 dic.get(
                                                                                                     'goods_price'))))
                            with open('兑换成功列表.txt', 'a', encoding='utf-8') as f:
                                f.write('{username}兑换成功 {goodsname}{num}个，兑换后积分{integral2}\n'.format(username=u,
                                                                                                     goodsname=goodsname,
                                                                                                     num=goods_num,
                                                                                                     integral2=integral - goods_num * int(
                                                                                                         dic.get(
                                                                                                             'goods_price'))))
                            return
    else:
        print("当前账号{u}积分不足".format(u=u))

if __name__ == '__main__':
    print('开始检查账号格式')
    with open('账号.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line:
                try:
                    name = line.split('----')[0].strip('\n')
                    pwd = line.split('----')[1].strip('\n')
                except:
                    print(line + '格式不对,程序退出')
                    sys.exit()
    print('账号检测通过')
    print("开始监测商品")
    S = SendRequest()
    u = '16733815003'
    p = '123456'
    S.login(u, p)
    while True:
        sleep(random.uniform(0.5, 1.5))
        res = S.get_goods_list()
        print('商品发放监测中...')
        if res:
            #print(res)
            print('商品发放成功，开始抢购')
            break
    with open('账号.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line:
                try:
                    name = line.split('----')[0].strip('\n')
                    pwd = line.split('----')[1].strip('\n')
                    #print(1231232132132132)
                    goods_duihuan(name, pwd)
                except:
                    print("用户name不存在，或者账户被禁用")
                    print(line + '格式不对')

