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


def fred_data_download(index_dict, url):
    fred_data = pd.DataFrame()
    describes = []
    error_list = []
    for signal in index_dict.keys():
        try:
            newsignal = pd.DataFrame(fred.get_series(index_dict.get(signal)), columns=[signal])
            fred_data = pd.concat([fred_data, newsignal], axis=1)
        except:
            error_list.append(('data error:', signal))
            continue
        try:
            re = requests.get(url + index_dict.get(signal)).text
            soup = BeautifulSoup(re, 'html.parser')
            series_notes = soup.find(class_='series-notes').get_text()
            describes.append((signal, series_notes))
        except:
            error_list.append(('describes error:', signal))
            continue
    data_describes = pd.DataFrame(describes, columns=['signal', 'describe']).set_index('signal')
    return fred_data, data_describes, error_list


if __name__ == '__main__':
    url = 'https://fred.stlouisfed.org/series/'
    index_dict = {'SP500': 'SP500',
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
                  'Consumer Sentiment': 'UMCSENT',
                  'Consumer Opinion Surveys: Confidence Indicators': 'CSCICP03USM665S',
                  'GDP': 'GDP',
                  'Consumer Price Index: Used Cars and Trucks in U.S.': 'CUSR0000SETA02',
                  'Personal Consumption Expenditures': 'PCE',
                  'Inflation Expectation': 'MICH'
                  }

    data, describe, error_list = fred_data_download(index_dict, url)
    print(data)
    print(describe)
    print('error_list:', error_list)
