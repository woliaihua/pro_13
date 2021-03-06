from helium import *
import configparser
import os
import chardet
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from time import sleep
import cv2
import requests
from PIL import Image
from  selenium import webdriver
from  io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains

"""
滑动图片验证
"""

def get_file_code(filename):
    f3 = open(filename, 'rb')
    data = f3.read()
    encode = chardet.detect(data).get('encoding')
    f3.close()
    return encode

#path1 = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录
path2 ='config.ini'
encode = get_file_code(path2)
config = configparser.RawConfigParser()
config.read(path2, encoding=encode)
chrome_path = config.get('month', "chrome_path")  # 0-12 如果是0 就表示不指定月份

port =9027
kill_pid(port)
# 关闭进程
cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(chrome_path=chrome_path,port=port)  # --headless
os.popen(cmd)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}".format(port=port))
driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=chrome_options)
script = '''
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
'''
set_driver(driver)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
driver.get('http://yqdz.meiri100.cn/mall/index')
write('17045171640',into=S('//*[@id="username"]'))
write('123456',into=S('//*[@id="password"]'))
#click('登录')
#driver.get('http://yqdz.meiri100.cn/mall/index')
#wait_until(S('//*[@id="list"]/li[@goods_name="300元京东卡"]//button[contains(text(),"立即购买")]').exists, timeout_secs=0.2, interval_secs=0.2)

