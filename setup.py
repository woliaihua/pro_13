from helium import *
from time import sleep
import configparser
from itertools import zip_longest
import chardet
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import functools
from itertools import zip_longest
from locale import atof, setlocale, LC_NUMERIC
from jifen_2_goods import get_suds2
from send_request import SendRequest
import re

setlocale(LC_NUMERIC, 'English_US')


def get_file_code(filename):
    f3 = open(filename, 'rb')
    data = f3.read()
    encode = chardet.detect(data).get('encoding')
    f3.close()
    return encode


# path1 = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录
path2 = 'config.ini'
encode = get_file_code(path2)
config = configparser.RawConfigParser()
config.read(path2, encoding=encode)
chrome_path = config.get('month', "chrome_path")  # 0-12 如果是0 就表示不指定月份
state = config.get('month', "state")
pool_num = config.get('month', "pool_num")


def decorator(func):
    @functools.wraps(func)
    def wrapper(args):
        try:
            return func(*args)
        except Exception as e:
            raise e

    return wrapper

class BaseStartChome():
    """
    反爬模式启动浏览器
    """

    def __init__(self, port):
        kill_pid(port)
        # 关闭进程
        self.cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(
            chrome_path=chrome_path, port=port)  # --headless
        os.popen(self.cmd)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}".format(port=port))
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        set_driver(self.driver)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        Config.implicit_wait_secs = 11  # 设置隐式等待时间15秒
        self.login_out()

    def login(self, u, p):
        """
        登录
        :param u:用户名
        :param p:密码
        :return:
        """
        self.name = u.strip('\n')
        self.pwd = p.strip('\n')
        print('开始执行账号{}'.format(u))
        self.driver.get(
            'http://yqdz.meiri100.cn/login/index?group_id=7b08022526618cf1eab62a8f81c6c437')
        write(u, into=S('//*[@id="username"]'))
        write(p, into=S('//*[@id="password"]'))
        click(Button('登录'))
        state = self.chick_login()
        if state:
            print(self.name + ' 登录成功')
            print('开始检测并清空购物车')
            self.clear_cart()
            return True
        else:
            return False

    def chick_login(self):
        sleep(1.5)
        url = self.driver.current_url
        if 'taskIssue' in url:
            return True
        else:
            return False

    def get_integral(self):
        """
        获取积分
        :return:int 积分
        """
        S = SendRequest()
        S.login(self.name, self.pwd)
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

    def clear_cart(self):
        """
        清空购物车
        :return:
        """
        self.driver.get('http://yqdz.meiri100.cn/mall/index')
        num = int(S('//*[@id="cart_goodsSpecies_num"]').web_element.text)
        if num != 0:
            self.driver.get('http://yqdz.meiri100.cn/Mall/cart_info#')
            click(S('//div[@class="detailBottomBox"]/i'))
            click(S('//a[contains(text(),"确定")]'))

    def click_buy(self, l2, first=False):
        """
        购买流程
        :param l2: ini配置的可购买的东西
        :param first: 是否第一次请求，第一次就不用刷新 页面，提高效率
        :return:
        """
        if not first:
            self.driver.get('http://yqdz.meiri100.cn/mall/index')
        integral = self.get_integral()  # 获取积分
        print("当前积分：",integral)
        l = get_suds2(integral, l2)  # 获取可以购买的商品与个数 [('300元京东卡', 1, 30000), ('100元京东卡', 1, 10000)]
        if not l:
            return
        for index, (name, goods_num, base_integral) in enumerate(l):
            try:
                self.driver.find_elements_by_xpath(
                    '//*[@id="list"]/li[@goods_name="{}"]//button[contains(text(),"立即购买")]'.format(name))[0].click()
                for i in range(int(goods_num)-1):  # 输入个数
                    click(S('//button[@class="add_btn"]'))
                click('确认兑换')
                print('{username}点击确认兑换成功 {goodsname}{num}个，兑换前积分{integral2}'.format(username=self.name,
                                                                                            goodsname=name,
                                                                                            num=goods_num,
                                                                                            integral2=integral))
                with open('兑换成功列表.txt', 'a', encoding='utf-8') as f:
                    f.write('{username}兑换成功 {goodsname}{num}个，兑换前积分{integral2}\n'.format(username=self.name,
                                                                                        goodsname=name,
                                                                                        num=goods_num,
                                                                                        integral2=integral))
                sleep(5)
                integral2 = self.get_integral()  # 再次获取积分
                l = get_suds2(integral2, l2)
                if not l:  # 积分不足以兑换商品
                    return
                break
            except:
                if '/mall/index' in self.driver.current_url:  # 说明抢购界面已无货，显示已兑完
                    l2 = l2.remove(l2[index])
                else:
                    self.clear_cart()
                    l2 = l2.remove(l2[index])
            finally:
                self.click_buy(l2)

    def exchange_service(self):
        """
        兑换京东卡流程，从服务检测
        :return:
        """
        S = SendRequest()
        S.login(self.name, self.pwd)
        S.get_goods_list()  # 有商品才会执行下一步
        self.driver.refresh()
        l2 = [('300元京东卡', 30000), ('100元京东卡', 10000), ('50元京东卡', 5000), ('20元京东卡', 2000)]
        self.click_buy(l2, True)
        self.exchange_service()


    def login_out(self):
        self.driver.delete_all_cookies()

    def accept_task(self):

        """
        接受任务
        :return:
        """
        self.driver.get('http://yqdz.meiri100.cn/taskIssue/index')
        try:
            xpath = '//div[@class="task_list"]//span[@class="button_span1" ]/span[not(contains(text(),"转发"))]'
            wait_until(S(xpath).exists, timeout_secs=1, interval_secs=0.5)  # 判断是否有非转发的任务存在
            xpath = '//div[@class="task_list"]//span[@class="button_span1" ]/span[not(contains(text(),"转发"))]/../../../..'
            # wait_until(S(xpath).exists, timeout_secs=1.5, interval_secs=0.5)
            eles = find_all(S(xpath))
            hrefs = []
            for ele in eles:
                href = ele.web_element.get_attribute('href')
                hrefs.append(href)
            for href in hrefs:
                self.driver.get(href)
                title = S('//div/h1').web_element.text
                _type = S('//span[3][@class="address"]').web_element.text
                click(S('//button[contains(text(),"领取任务")]'))
                try:
                    with open('已接任务.txt', 'a', encoding='utf-8') as f:
                        f.write('账号：{name}  类型：{_type} 标题：{title} \n'.format(name=self.name, _type=_type, title=title))
                except:
                    pass
        except:
            pass


@decorator
def start_exchange_integral(port, line):
    """
    一个端口启动一个浏览器，一个浏览器只打开一个账号
    :param port: 端口
    :param line: 账号密码('16531009626----123456\n')
    :return:
    """

    B = BaseStartChome(port)
    if line:
        try:
            name = line.split('----')[0].strip('\n')
            pwd = line.split('----')[1].strip('\n')
        except:
            name = ''
            pwd = ''
            print(line + '格式不对')
        if name:
            login_state = B.login(name, pwd)
            if login_state:
                B.exchange()
            else:
                print('账号{name}登录失败，请检查账号密码'.format(name=name))


@decorator
def start_accept_task(port, txt_lines):
    """
    多进程领取任务
    :param port: 端口，一个端口启动一个浏览器
    :param txt_lines:账号密码 ('16531009626----123456\n', '17138959436----521000\n')
    :return:
    """

    #
    def accept_task(B, name, pwd):
        B.login(name, pwd)  # 登录
        login_state = B.login(name, pwd)
        if not login_state:
            print('账号{name}登录失败，请检查账号密码'.format(name=name))
            return
        B.accept_task()  # 领取任务
        B.login_out()  # 退出登录

    B = BaseStartChome(port)
    for line in txt_lines:
        if line:
            try:
                name = line.split('----')[0].strip('\n')
                pwd = line.split('----')[1].strip('\n')
            except:
                name = ''
                pwd = ''
                print(line + '格式不对')
            if name:
                accept_task(B, name, pwd)


if __name__ == '__main__':
    with open('账号.txt', 'r', encoding='utf-8') as f:
        txt_lines = f.readlines()
    start_accept_task((9022, txt_lines))
