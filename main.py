from multiprocessing import Process, Queue

import downloader as downloader  # 引入上面的新模块
import spiders.baidu as baidu
import spiders.bing as bing
import spiders.so as so
import spiders.sogo as sogo


def run_spider(target_func, keyword, cnt, que):
    """包装函数，用于启动爬虫进程"""
    try:
        target_func(keyword, cnt, que)
    except Exception as e:
        print(f"爬虫进程出错: {e}")

if __name__ == '__main__':
    # 确保在 Windows 下正常运行
    que = Queue()
    
    keyword = input("请输入关键词: ")
    # 增加输入校验
    try:
        cnt = int(input("请输入每个引擎爬取数量: "))
    except ValueError:
        cnt = 50
        print("输入无效，默认设置为 50")

    producers = [
        Process(target=run_spider, args=(baidu.spider, keyword, cnt, que)),
        Process(target=run_spider, args=(bing.spider, keyword, cnt, que)),
        Process(target=run_spider, args=(sogo.spider, keyword, cnt, que)),
        Process(target=run_spider, args=(so.spider, keyword, cnt, que))
    ]

    # 定义消费者（下载器）- 开启 4 个进程下载
    consumers = [Process(target=downloader.download_img, args=(que,)) for _ in range(4)]

    print("--- 开始爬取 ---")
    
    # 启动所有进程
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    # 等待所有爬虫生产完毕
    for p in producers:
        p.join()
    
    print("--- 爬虫任务完成，等待图片下载结束 ---")

    # 发送结束信号 (有多少个消费者就发送多少个 None)
    for _ in range(len(consumers)):
        que.put(None)

    # 等待下载完成
    for c in consumers:
        c.join()

    print("--- 全部任务结束 ---")