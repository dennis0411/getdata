from fredapi import Fred
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import os

# 填入專屬 API，讓 fredapi 核准會員通過
api_key = '4cc5831f733fba2032b5efe47e2132cb'


# path = os.path.expanduser("~/Desktop")


def test(api_key):
    fred = Fred(api_key)
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


def download_fred_data(index_dict, api_key):
    fred = Fred(api_key)
    url = 'https://fred.stlouisfed.org/series/'
    fred_data = pd.DataFrame()
    describes = []
    error_list = []
    for signal in index_dict.keys():
        try:
            new_signal = pd.DataFrame(fred.get_series(index_dict.get(signal)), columns=[signal])
            fred_data = pd.concat([fred_data, new_signal], axis=1)
        except:
            error_list.append(('data error:', signal))
            continue
        try:
            link = url + index_dict.get(signal)
            re = requests.get(link).text
            soup = BeautifulSoup(re, 'html.parser')
            describe = soup.find(class_='series-notes').get_text()
            describes.append((signal, describe, link))
        except:
            error_list.append(('describes error:', signal))
            continue
    data_describes = pd.DataFrame(describes, columns=['signal', 'describe', 'link']).set_index('signal')
    error_list = pd.DataFrame(error_list)
    return fred_data, data_describes, error_list


if __name__ == '__main__':
    index_dict = {'SP500': 'SP500',
                  'NASDAQ 100 Index': 'NASDAQ100',
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
                  'Consumer Price Index for All Urban Consumers: All Items in U.S. City Average': 'CPIAUCSL',
                  'Personal Consumption Expenditures': 'PCE',
                  'Inflation Expectation': 'MICH',
                  'Real M2 Money Stock': 'M2REAL',
                  'Velocity of M2 Money Stock': 'M2V',
                  'Personal Consumption Expenditures: Durable Goods': 'PCEDG',
                  'Personal Consumption Expenditures: Services': 'PCES',
                  'Personal Consumption Expenditures: Nondurable Goods': 'PCEND',
                  'Personal consumption expenditures: Food': 'DFXARC1M027SBEA',
                  'Personal consumption expenditures: Services: Health care': 'DHLCRC1Q027SBEA',
                  'Personal consumption expenditures: Durable goods: Motor vehicles and parts': 'DMOTRC1Q027SBEA',
                  'Personal consumption expenditures: Energy goods and services': 'DNRGRC1M027SBEA',
                  'Personal consumption expenditures: Clothing, footwear, and related services': 'DCAFRC1A027NBEA',
                  'Personal consumption expenditures: Pets, pet products, and related services': 'DPETRC1A027NBEA',
                  'Personal consumption expenditures: Services: Housing and utilities': 'DHUTRC1Q027SBEA',
                  'Unemployment Rate': 'UNRATE',
                  'Manufacturer New Orders: Total Manufacturing': 'AMTMNO',
                  'Manufacturer New Orders: Nondefense Capital Goods Excluding Aircraft': 'NEWORDER',
                  'Manufacturer New Orders: Durable Goods': 'DGORDER',
                  'Manufacturer New Orders: Consumer Durable Goods': 'ACDGNO',
                  'Manufacturer New Orders: Computers and Electronic Products': 'A34SNO',
                  'Manufacturer New Orders: Consumer Goods': 'ACOGNO',
                  'Manufacturer New Orders: Machinery': 'A33SNO',
                  'Manufacturer New Orders: Fabricated Metal Products': 'A32SNO',
                  'Manufacturer New Orders: Electrical Equipment, Appliances and Components': 'A35SNO',
                  'Manufacturer New Orders: Primary Metals': 'A31SNO',
                  'Manufacturer New Orders: Motor Vehicles and Parts': 'AMVPNO',
                  'Manufacturer New Orders: Furniture and Related Products': 'A37SNO',
                  'Manufacturer New Orders: Transportation Equipment': 'A36SNO',
                  'Manufacturer New Orders: Information Technology Industries': 'AITINO',
                  'Manufacturer New Orders: Industrial Machinery Manufacturing': 'A33ENO',
                  'Manufacturer New Orders: Nondefense Aircraft and Parts': 'ANAPNO',
                  'Manufacturer New Orders: Communications Equipment': 'A34XNO',
                  'Manufacturer New Orders: Ships and Boats': 'A36ZNO',
                  'Retail Money Market Funds': 'WRMFNS',
                  'Total Borrowings from the Federal Reserve': 'BORROW',
                  'CBOE Emerging Markets ETF Volatility Index': 'VXEEMCLS',
                  'New Privately-Owned Housing Units Started: Total Units': 'HOUST',
                  'S&P/Case-Shiller U.S. National Home Price Index': 'CSUSHPISA',
                  'Auto Inventory/Sales Ratio': 'AISRSA',
                  'Domestic Auto Inventories': 'AUINSA',
                  'Retailers Inventories': 'RETAILIMSA',
                  'Merchant Wholesalers Inventories': 'WHLSLRIMSA',
                  'Manufacturers Total Inventories: Total Manufacturing': 'AMTMTI',
                  'Corporate Profits After Tax': 'CP',
                  'Total Business: Inventories to Sales Ratio': 'ISRATIO',
                  'Manufacturers: Inventories to Sales Ratio': 'MNFCTRIRSA',
                  'Manufacturers Inventories to Shipments Ratios: Total Manufacturing': 'AMTMIS',
                  'Retailers: Inventories to Sales Ratio': 'RETAILIRSA',
                  'Merchant Wholesalers: Inventories to Sales Ratio': 'WHLSLRIRSA',
                  'Retail Inventories/Sales Ratio: Motor Vehicle and Parts Dealers': 'MRTSIR441USS',
                  'Retail Inventories/Sales Ratio: Food and Beverage Stores': 'MRTSIR445USS',
                  'Total Business Sales': 'TOTBUSSMSA',
                  'Total Business Inventories': 'BUSINV',
                  'Nonfinancial Business; Total Capital Expenditures, Transactions': 'BOGZ1FA145050005Q',
                  'Mutual Funds and Exchange-Traded Funds; Corporate Equities; Asset, Transactions': 'BOGZ1FA483064105Q',
                  'Mutual Funds; Corporate Equities; Asset, Transactions': 'BOGZ1FA653064100Q',
                  'ICE BofA AAA US Corporate Index Effective Yield': 'BAMLC0A1CAAAEY',
                  'ICE BofA AA US Corporate Index Effective Yield': 'BAMLC0A2CAAEY',
                  'ICE BofA Single-A US Corporate Index Effective Yield': 'BAMLC0A3CAEY',
                  'ICE BofA BBB US Corporate Index Effective Yield': 'BAMLC0A4CBBBEY',
                  'ICE BofA US High Yield Index Effective Yield': 'BAMLH0A0HYM2EY',
                  'ICE BofA BB US High Yield Index Effective Yield': 'BAMLH0A1HYBBEY',
                  'ICE BofA Single-B US High Yield Index Effective Yield': 'BAMLH0A3HYCEY',
                  'ICE BofA CCC & Lower US High Yield Index Effective Yield': 'BAMLH0A1HYBBEY',
                  'ICE BofA 1-3 Year US Corporate Index Effective Yield': 'BAMLCC0A0CMTRIV',
                  'ICE BofA 3-5 Year US Corporate Index Effective Yield': 'BAMLC2A0C35YEY',
                  'ICE BofA 5-7 Year US Corporate Index Effective Yield': 'BAMLCC0A0CMTRIV',
                  'ICE BofA 7-10 Year US Corporate Index Effective Yield': 'BAMLC4A0C710YEY',
                  'ICE BofA 10-15 Year US Corporate Index Effective Yield': 'BAMLC7A0C1015YEY',
                  'ICE BofA 15+ Year US Corporate Index Effective Yield': 'BAMLC8A0C15PYEY',
                  'ICE BofA 1-3 Year US Corporate Index Total Return Index Value': 'BAMLCC1A013YTRIV',
                  'ICE BofA 3-5 Year US Corporate Index Total Return Index Value': 'BAMLCC2A035YTRIV',
                  'ICE BofA 5-7 Year US Corporate Index Total Return Index Value': 'BAMLCC3A057YTRIV',
                  'ICE BofA 7-10 Year US Corporate Index Total Return Index Value': 'BAMLCC4A0710YTRIV',
                  'ICE BofA 10-15 Year US Corporate Index Total Return Index Value': 'BAMLCC7A01015YTRIV',
                  'ICE BofA 15+ Year US Corporate Index Total Return Index Value': 'BAMLCC8A015PYTRIV',
                  'ICE BofA US Corporate Index Total Return Index Value': 'BAMLCC0A0CMTRIV',
                  'ICE BofA US High Yield Index Total Return Index Value': 'BAMLHYH0A0HYM2TRIV',
                  'ICE BofA CCC & Lower US High Yield Index Total Return Index Value': 'BAMLHYH0A3CMTRIV',

                  }

    data, describe, error_list = download_fred_data(index_dict, api_key)
    print('error_list:', error_list)

    excel_name = 'fred.xlsx'
    path = os.path.join(os.getcwd(), excel_name)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    data.to_excel(writer, sheet_name='data')
    describe.to_excel(writer, sheet_name='describe')
    error_list.to_excel(writer, sheet_name='error_list')
    writer.save()


