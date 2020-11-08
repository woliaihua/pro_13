import functools
from itertools import zip_longest
from multiprocessing import Pool
from multiprocessing import freeze_support

# 文件对象是迭代器。要一次迭代文件N行，与线程数一致，一次迭代N行就执行多少个线程
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class B():
    pass

def decorator(func):
    @functools.wraps(func)
    def wrapper(args):
        try:
            return func(*args)
        except Exception as e:
            raise e
    return wrapper

@decorator
def start(port,txt_lines):
    """

    :param port: 启动端口
    :param name1: lines
    :return:
    """
    pass


if __name__ == '__main__':


    N = 2  # 进程数
    pool = Pool(N)
    with open('账号.txt','r',encoding='utf-8') as f:
        txt_lines = f.readlines()
    #每个进程平均分配账号
    shang,yu = divmod(len(txt_lines),N)
    l = []
    for lines in grouper(txt_lines,shang+1):
        l.append(lines)
    list_args = list(zip(range(9022,9022+N),l))
    pool.map(start_accept_task,list_args)