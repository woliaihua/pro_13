
import datetime
print(datetime.datetime.now())
response_1 = [{'goods_status': 1, 'goods_name': '100元京东卡',
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

for dic in response_1:
    if '50元京东卡' == dic.get('goods_name'):
        print(222222222222)
        goods_num =2
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
            print(data)
print(datetime.datetime.now())