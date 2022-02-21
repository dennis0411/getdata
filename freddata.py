from fredapi import Fred
from getdata import ToExcel
import requests
import numpy as np
import pandas as pd
import datetime as dt
import os

# 填入專屬 API，讓 fredapi 核准會員通過
api_key = '4cc5831f733fba2032b5efe47e2132cb'
path = os.path.expanduser("~/Desktop")
fred = Fred(api_key)

# 先取得 FRED 大分類的完整資訊
r = requests.get('https://api.stlouisfed.org/fred/releases?api_key=' + api_key + '&file_type=json', verify=True)
full_releases = r.json()['releases']

# 轉成 DataFrame，來看看這份完整資料長怎樣
full_releases = pd.DataFrame.from_dict(full_releases)

# 將『大分類 ID』放在 index，方便後面的搜尋作業
full_releases = full_releases.set_index('id')

# 提供一個從大分類表中進行關鍵字搜尋的程式碼，方便大家查詢需要的大分類，我們以『gdp』作為示範
search_keywords = 'gdp'
search_result = full_releases.name[full_releases.name.apply(lambda x: search_keywords in x.lower())]

# 創造一個以季為更新單位總表
econ_data = pd.DataFrame(index=pd.date_range(start='2000-01-01', end=dt.datetime.today(), freq='QS'))

# 開始迴圈爬資料：
#  第一層迴圈（大分類）：
#   每個大分類底下，篩選出『最熱門的前三子項目』，以及相對應的『子項目英文代碼』
#   (當然也可以整個 FRED 所有項目內容都爬取下來，這邊僅做示範)
# 第二層迴圈（子項目）：
#  陸續將每一個項目放入該總表裡面，完成你的經濟數據庫！
for release_id in search_result.index:
    release_topic = search_result[release_id]
    series_df = fred.search_by_release(release_id, limit=3, order_by='popularity', sort_order='desc')
    for topic_label in series_df.index:
        econ_data[series_df.loc[topic_label].title] = fred.get_series(topic_label, observation_start='2000-01-01',
                                                                      observation_end=dt.datetime.today())

ToExcel(path, 'econ_data.xlsx', econ_data, 'fred')

