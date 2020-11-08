
import configparser
import chardet
from locale import atof,setlocale,LC_NUMERIC
setlocale(LC_NUMERIC, 'English_US')

def get_file_code(filename):
    f3 = open(filename, 'rb')
    data = f3.read()
    encode = chardet.detect(data).get('encoding')
    f3.close()
    return encode

path2 ='config.ini'
encode = get_file_code(path2)
config = configparser.RawConfigParser()
config.read(path2, encoding=encode)
state = config.get('month', "state")


def get_suds2(num,l2):
    """
    每次提交购物车只能一种商品，并且不能大于5
    :param num: 用户剩余积分
    :param l2: 用户可兑换的数据[('300元京东卡', 30000), ('100元京东卡', 10000), ('50元京东卡', 5000), ('20元京东卡', 2000)])
    :return:[('300元京东卡', 1, 30000), ('100元京东卡', 1, 10000), ('50元京东卡', 1, 5000)]
    """
    dic = []
    def get_sud(num):
        for index,(name,integral) in enumerate(l2):
            shang,yu = divmod(num,integral)
            if shang==0:
                continue
            elif shang>5:
                shang = 5
            if state == 'N':
                if name == '20元京东卡':
                    continue
            dic.append((name,shang,integral))
            num = num-int(integral)*shang
            l2.remove(l2[index])
            get_sud(num)
            break
    get_sud(num)
    return dic
if __name__ == '__main__':
    import datetime
    print(datetime.datetime.now())
    l2 = [('300元京东卡', 30000), ('100元京东卡', 10000), ('50元京东卡', 5000), ('20元京东卡', 2000)]
    print(get_suds2(45077,l2))
    # for k,v,integral in get_suds2(100000,l2):
    #     print(k,v,integral)
    print(datetime.datetime.now())