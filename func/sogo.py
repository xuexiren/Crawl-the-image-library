import asyncio
import time

import aiohttp
from sortedcontainers import SortedSet

import func.common


async def get_img_url(url, headers, params, imgs_list, que, cnt):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params, verify_ssl=False) as response:
            json_data = await response.json();
            data_list = json_data['data']['items'];
            for data in data_list:
                img_url = data['oriPicUrl'];
                if len(imgs_list) >= int(cnt):
                    return
                if img_url not in imgs_list:
                    que.put([img_url, f'sogo{len(imgs_list)}'])
                    imgs_list.add(img_url)
                    print(f'图片{img_url}获取成功')
                    time.sleep(0.5)


def spider(keyword, cnt, que):
    url = 'https://pic.sogou.com/napi/pc/searchList'
    imgs_list = SortedSet()
    page = 1
    step = 2

    while len(imgs_list) < int(cnt):
        task_list = []
        for idx in range(page, page + step):
            params = (
                ('mode', '1'),
                ('start', idx * 48),
                ('xml_len', '48'),
                ('query', keyword),
                ('channel', 'pc_pic'),
                ('scene', 'pic_result'),
            )
            new_headers = func.common.headers
            new_headers['X-Time4p'] = str(int(time.time() * 1000))
            c = get_img_url(url=url, headers=new_headers, params=params, imgs_list=imgs_list, que=que, cnt=cnt)
            task = asyncio.ensure_future(c)
            task_list.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task_list))
        page += step
        # step *= 2
