import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


def download_img(que):
    while True:
        if que.empty():
            continue
        temp = que.get()
        img_url = temp[0]
        img_name = temp[1] + '.jpg'
        with open(f'./img/{img_name}', 'wb') as fp:
            with requests.get(img_url, headers=headers, verify=False, timeout=(3, 7)) as r:
                img_data = r.content
            fp.write(img_data)
        print(f'图片{img_name}下载完成')
