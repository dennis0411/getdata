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

def downloadfreddata(api_key):
    r = requests.get('https://api.stlouisfed.org/fred/releases?api_key=' + api_key + '&file_type=json', verify=True)
    full_releases = r.json()['releases']

    full_releases = pd.DataFrame.from_dict(full_releases)

    full_releases = full_releases.set_index('id')

    search_keywords = 'gdp'
    search_result = full_releases.name[full_releases.name.apply(lambda x: search_keywords in x.lower())]

    econ_data = pd.DataFrame(index=pd.date_range(start='2000-01-01', end=dt.datetime.today(), freq='QS'))

    for release_id in search_result.index:
        release_topic = search_result[release_id]
        series_df = fred.search_by_release(release_id, limit=3, order_by='popularity', sort_order='desc')
        for topic_label in series_df.index:
            econ_data[series_df.loc[topic_label].title] = fred.get_series(topic_label, observation_start='2000-01-01', observation_end=dt.datetime.today())

    return econ_data

# econ_data = downloadfreddata(api_key)
# ToExcel(path, 'econ_data.xlsx', econ_data, 'fred')



data = fred.get_series('SP500')
print(data)

