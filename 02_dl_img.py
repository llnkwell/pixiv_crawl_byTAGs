import time

import requests
import pandas as pd
from concurrent.futures import wait, ALL_COMPLETED, ThreadPoolExecutor
from requests.exceptions import ProxyError

with open('cookie.txt', mode='r') as f:
    cookie = f.read()

headers = {
    "accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36',
    # "Cookie": cookie,
    'referer': "https://www.pixiv.net/",
}

proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

failed_set = set()


def get_url(df):
    dl_list = []
    for url, pageCount in zip(df['url'], df['pageCount']):
        f_url = url.split('/img/')[1].split('_', 1)[0]
        for page in range(pageCount):
            dl_list.append(f'https://i.pximg.net/img-original/img/{f_url}_p{page}.png')
    return dl_list


def download_image(img_url):
    fail = open("failed.csv", mode="a+")
    try:
        ill_rec = requests.get(img_url, headers=headers, proxies=proxy)
        if ill_rec.status_code == 404:
            ill_rec = requests.get(img_url.replace('png', 'jpg'), headers=headers, proxies=proxy)
        ill_file = ill_rec.content
        filename = ill_rec.url.rsplit('/', 1)[1]
        ill_rec.close()
        with open("D:\\image\\" + filename, "wb") as image:
            image.write(ill_file)
            image.close()
        print(ill_rec.status_code, ill_rec.url)
    except ProxyError:
        print(img_url, "failed!")
        fail.write(img_url)
        time.sleep(2)
        pass


if __name__ == '__main__':
    ill_info = pd.read_csv("json.csv")

    dl_df = pd.DataFrame()
    dl_df['id'] = ill_info['id']
    dl_df['url'] = ill_info['url']
    dl_df['xRestrict'] = ill_info['xRestrict']
    dl_df['pageCount'] = ill_info['pageCount']
    dl_df = dl_df[dl_df['xRestrict'] == 0]
    dl_df = dl_df.drop('xRestrict', axis=1)

    direct_list = get_url(dl_df)

    executor_download = ThreadPoolExecutor(max_workers=4)
    download_task = [executor_download.submit(download_image, i) for i in direct_list]
    wait(download_task, return_when=ALL_COMPLETED)
    # for i in imgUrl_list:
    #     download_image(i)
    #     time.sleep(1)
    print('\n All downloaded!')
