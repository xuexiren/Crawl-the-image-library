import asyncio
import time

import aiohttp
from sortedcontainers import SortedSet

import func.common


async def get_img_url(url, headers, params, imgs_list, que, cnt):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params, verify_ssl=False) as response:
            json_data = await response.json()
            data_list = json_data['data']
            for data in data_list[:-1]:
                img_url = data['middleURL']
                if len(imgs_list) >= int(cnt):
                    return
                if img_url not in imgs_list:
                    que.put([img_url, f'baidu{len(imgs_list)}'])
                    imgs_list.add(img_url)
                    print(f'图片{img_url}获取成功')
                    time.sleep(0.5)


def spider(keyword, cnt, que):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7815540444006395368&ipn=rj&ct=201326592&is=&fp=result&fr=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&rn=30&gsm=5a&1721369566298=';
    imgs_list = SortedSet()
    page = 1
    step = 2
    while len(imgs_list) < int(cnt):
        task_list = []
        for idx in range(page, page + step):
            params = (
                ('word', keyword),
                ('queryWord', keyword),
                ('pn', page * 30)
            )
            c = get_img_url(url=url, headers=func.common.headers, params=params, imgs_list=imgs_list, que=que, cnt=cnt)
            task = asyncio.ensure_future(c)
            task_list.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task_list))
        page += step
        # step *= 2
