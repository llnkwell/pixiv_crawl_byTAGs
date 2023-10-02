import time
import requests
import pandas as pd
from requests.exceptions import ProxyError

with open('./cookie', mode='r') as f:
    cookie = f.read()

headers0 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/97.0.4692.71 Safari/537.36", 'referer': "https://www.pixiv.net/",
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "cookie": cookie}

proxy0 = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

TAG = "ブルーアーカイブ"  # 此处输入搜索标签，多个标签之间以空格分隔


def img_url(tag0, p0):
    # monthly url
    url = f"https://www.pixiv.net/ajax/search/illustrations/{tag0}?word={tag0}&order=date_d&mode=safe&scd=2023-09-01" \
          f"&ecd=2023-09-15&p={p0}&s_mode=s_tag&type=illust&ai_type=1&lang=zh"
    return url


def first_page(url0):
    try:
        pageContent = requests.get(url0, headers=headers0, proxies=proxy0)
        pageJson = pageContent.json()
        imgAmount = pageJson['body']['illust']['total']
        print(imgAmount, "img in all!")
        pageContent.close()
        pageDf = pd.DataFrame(pageJson['body']['illust']['data'])
        pageDf.to_csv("./data/imgJson.csv", mode='a+', header=True, index=False)
        return imgAmount
    except ProxyError:
        print("NetworkError!")


def each_page(tag0, p0):
    url0 = img_url(tag0, p0)
    pageContent = requests.get(url0, headers=headers0, proxies=proxy0)
    pageJson = pageContent.json()
    pageContent.close()
    pageDf = pd.DataFrame(pageJson['body']['illust']['data'])
    pageDf.to_csv("./json.csv", mode='a+', header=False, index=False)
    print("page", p0, "done.")


if __name__ == '__main__':
    tags = TAG
    p = 1
    monthlyUrl = img_url(tags, p)
    # print(monthlyUrl)
    amount = first_page(monthlyUrl)
    p += 1
    while True:
        try:
            each_page(tags, p)
            time.sleep(0.8)
            p += 1
        except requests.RequestException:
            print("\npage", p, "error!")
            time.sleep(2)
            pass
        if p > amount / 60 + 2:
            print("All jsons done.")
            break
