from requests.exceptions import ProxyError
import pandas as pd
import requests
import time

tag = 'ブルーアーカイブ'  # input('Please enter the tags sep with block: \n')
page = 1
list_url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date&mode=all&p={page}&s_mode' \
           f'=s_tag&type=all&lang=zh'

with open('cookie.txt', mode='r') as f:
    cookie = f.read()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/97.0.4692.71 Safari/537.36", 'referer': "https://www.pixiv.net/",
           'cookie': cookie}

proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
names = []


def get_amount(init_url):
    rec = requests.get(init_url, headers=headers, proxies=proxy)
    p_list = rec.json()
    total = p_list['body']['illustManga']['total']
    print(tag, "has", total, "pics in total! so many!!", end='')
    rec.close()
    if total / 60 > total // 60:
        pages = total // 60 + 1
    else:
        pages = total // 60
    print("And get", pages, "pages!")
    p_df = pd.DataFrame(p_list['body']['illustManga']['data'])
    names.extend(p_df.columns)
    return pages


def get_json(each_json_url):
    json_raw = requests.get(each_json_url, headers=headers, proxies=proxy)
    p_json = json_raw.json()
    p_df = pd.DataFrame(p_json['body']['illustManga']['data'])
    p_df.to_csv("json.csv", mode="a+", header=False, index=False)


if __name__ == '__main__':
    p_pages = get_amount(list_url)
    p = 1
    while True:
        p_url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date&mode=all&p={p}&s_mode' \
                f'=s_tag&type=all&lang=zh'
        try:
            get_json(p_url)
            if p <= p_pages:
                print("get page", p, "success!")
                time.sleep(2)
                p += 1
            else:
                print("ALL done!")
                break
        except ProxyError:
            print("Network error!")
            pass

# json0 = pd.read_csv("json.csv")
# json0.columns = names
# json0.to_csv("json.csv")
