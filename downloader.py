import os
import requests
import urllib3

# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 默认 Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def download_img(que):
    """
    下载进程执行的函数
    """
    if not os.path.exists('./imgs'):
        os.makedirs('./imgs', exist_ok=True)

    while True:
        # 阻塞式获取，避免 CPU 空转
        try:
            item = que.get() 
        except Exception:
            break

        # 结束信号
        if item is None:
            break

        img_url, img_name_prefix = item
        img_filename = f'{img_name_prefix}.jpg'
        file_path = f'./img/{img_filename}'
        
        # 简单的去重检查（可选）
        if os.path.exists(file_path):
            print(f'[跳过] {img_filename} 已存在')
            continue

        try:
            with requests.get(img_url, headers=HEADERS, verify=False, timeout=10) as r:
                if r.status_code == 200:
                    with open(file_path, 'wb') as fp:
                        fp.write(r.content)
                    print(f'[下载完成] {img_filename}')
                else:
                    print(f'[下载失败] {img_filename} 状态码: {r.status_code}')
        except Exception as e:
            print(f'[错误] 下载 {img_filename} 出错: {e}')