import os
from multiprocessing import Queue, Process

import urllib3

import func.baidu
import func.bing
import func.common
import func.so
import func.sogo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == '__main__':

    if not os.path.exists('./img'):
        make_dir = os.mkdir('./img')

    que = Queue()
    keyword = input("请输入关键词: ")
    cnt = input("请输入数量: ")

    p1 = Process(target=func.baidu.spider, args=(keyword, cnt, que))
    p2 = Process(target=func.bing.spider, args=(keyword, cnt, que))
    p3 = Process(target=func.sogo.spider, args=(keyword, cnt, que))
    p4 = Process(target=func.so.spider, args=(keyword, cnt, que))
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    c1 = Process(target=func.common.download_img, args=(que,))
    c2 = Process(target=func.common.download_img, args=(que,))
    c3 = Process(target=func.common.download_img, args=(que,))
    c4 = Process(target=func.common.download_img, args=(que,))
    c1.start()
    c2.start()
    c3.start()
    c4.start()
