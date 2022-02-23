from fredapi import Fred
from getdata import ToExcel
import requests
from bs4 import BeautifulSoup
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
            econ_data[series_df.loc[topic_label].title] = fred.get_series(topic_label, observation_start='2000-01-01',
                                                                          observation_end=dt.datetime.today())

    return econ_data


# econ_data = downloadfreddata(api_key)
# ToExcel(path, 'econ_data.xlsx', econ_data, 'fred')


def financial_signal(signal_dict, url):
    findex = pd.DataFrame()
    describe = []
    for signal in signal_dict.keys():
        newsignal = pd.DataFrame(fred.get_series(signal_dict.get(signal)), columns=[signal])
        findex = pd.concat([findex, newsignal], axis=1)
        re = requests.get(url + signal_dict.get(signal)).text
        soup = BeautifulSoup(re, 'html.parser')
        series_notes = soup.find(class_='series-notes').get_text()
        describe.append((signal, series_notes))
    describes = pd.DataFrame(describe, columns=['signal', 'describe']).set_index('signal')
    return findex, describes


# print(Findex.columns)
# print(Findex.tail(30))

if __name__ == '__main__':
    url = 'https://fred.stlouisfed.org/series/'
    signal_dict = {'SP500': 'SP500',
                   'VIX': 'VIXCLS',
                   'St. Louis Fed Financial Stress Index': 'STLFSI3',
                   'Federal Funds Effective Rate': 'DFF',
                   '10y minus 3m': 'T10Y3M',
                   'Economic Policy Uncertainty Index for United States': 'USEPUINDXD',
                   'Equity Market-related Economic Uncertainty Index': 'WLEMUINDXD',
                   'Equity Market Volatility Tracker: Overall': 'EMVOVERALLEMV',
                   'Chicago Fed National Financial Conditions': 'NFCI',
                   'Inflation Risk Premium': 'TENEXPCHAINFRISPRE',
                   'Real Risk Premium': 'TENEXPCHAREARISPRE',
                   }

    findex, describes = financial_signal(signal_dict, url)
    print(findex)
    print(describes)
