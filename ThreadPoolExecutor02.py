# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月18日
"""
# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月18日
"""
import time
from concurrent.futures import ThreadPoolExecutor


def task(str):
    print('正在打印', str)
    time.sleep(2)
    print('打印完成', str)
    return str


def callback(res):  # 必须有一个形参，来接收期程对象
    print(res.result())


sts = ['superficial', 'marvelous', 'magnificient', 'fabulous', 'jesus']
if __name__ == '__main__':
    my_list = []
    time1 = time.time()
    with ThreadPoolExecutor(max_workers=5) as pool:
        for str in sts:
            res = pool.submit(task, str)
            res.add_done_callback(callback)  # 增加回调函数,当期程对象中的任务处理状态完毕后将自动调用回调函数
        pool.shutdown(wait=True)
    time2 = time.time()
    print('执行时间：', time2 - time1)
