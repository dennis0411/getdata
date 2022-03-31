from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import urllib.parse
import threading
import pprint

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)


# 物件化
class cnyes_source():
    def __init__(self):
        self.news_url = {"us_stock": "https://news.cnyes.com/news/cat/us_stock",
                         "world_stock": "https://news.cnyes.com/news/cat/wd_stock",
                         "eu_asia_stock": "https://news.cnyes.com/news/cat/eu_asia_stock",
                         "taiwan_stock": "https://news.cnyes.com/news/cat/tw_stock",
                         "china_stock": "https://news.cnyes.com/news/cat/cn_stock",
                         "crypto": "https://news.cnyes.com/news/cat/bc",
                         "currency": "https://news.cnyes.com/news/cat/forex",
                         "futures": "https://news.cnyes.com/news/cat/future",
                         }
        self.news_data = pd.DataFrame()

    def get_url_list(self):
        for url in self.news_url.keys():
            target_url = url
            r = requests.get(target_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            for tag in soup.find_all(class_="_1Zdp"):
                href = tag.get('href')
                link = self.url + href
                url_list.append(link)
                market_list.append(submarket)
        self.news_data["market"] = market_list

        return url_list

    def download_data(self, url):
        for
        url =
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        news = " "
        tag = soup.find('time')
        datetime = tag.text.split(' ')
        t = datetime[1]
        d = datetime[0]
        source = 'cnyes'
        title = soup.h1.text

        for sub_tag in soup.find(class_="_1UuP"):
            for p in sub_tag.find_all('p'):
                a = p.text
                news += a

        data = {"target_url": target_url,
                "time": t,
                "date": d,
                "source": source,
                "title": title,
                "news": news,
                "link": target_url,
                "market": }



    def multi(self, url_list):
        threads = []
        for target_url in url_list:
            threads.append(threading.Thread(target=self.download_data, args=(target_url,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def write_db(self):
        print(f'Loading data from cnyes')
        list = self.get_url_list()
        self.multi(list)


