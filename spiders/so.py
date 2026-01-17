import asyncio
import re
import time

import aiohttp
from sortedcontainers import SortedSet

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

async def get_img_url(url, headers, params, imgs_list, que, cnt):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params, verify_ssl=False) as response:
            page_text = await response.text()
            s = re.findall('"thumb_bak":"(.*?)",', page_text)
            for img_url in s:
                img_url = img_url.replace('\\', '')  # 去除反斜杠
                if len(imgs_list) >= int(cnt):
                    return
                if img_url not in imgs_list:
                    que.put([img_url, f'so{len(imgs_list)}'])
                    imgs_list.add(img_url)
                    print(f'图片{img_url}获取成功')
                    time.sleep(0.5)


def spider(keyword, cnt, que):
    url = 'https://image.so.com/j'
    imgs_list = SortedSet()
    page = 1
    step = 2
    while len(imgs_list) < int(cnt):
        task_list = []
        for idx in range(page, page + step):
            params = (
                ('q', keyword),
                ('pd', '1'),
                ('pn', '60'),
                ('correct', keyword),
                ('sn', idx * 20),
            )
            c = get_img_url(url=url, headers=HEADERS, params=params, imgs_list=imgs_list, que=que, cnt=cnt)
            task = asyncio.ensure_future(c)
            task_list.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task_list))
        page += step
