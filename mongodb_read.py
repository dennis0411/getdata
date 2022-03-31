import pprint
import time
import pandas as pd
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
from pymongo import MongoClient
from warnings import simplefilter

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# 取消 future warning


simplefilter(action='ignore', category=FutureWarning)

# 引入密碼
path = "mongodb_password"
with open(path) as f:
    word = f.readline().split(',')
    account = word[0]
    password = word[1]

# mongodb connection
CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)


# db = client.getdata
# collection = db.fundament
# result1 = collection.find_one({'Ticker': 'BABA'})
# print(result1)
# result2 = collection.find(filter={'Sector': 'Technology'})
# for i in result2:
#     print(i['Market Cap'])

db = client.getdata
collection = db.bb
result = collection.find_one({'name' : 'spx'})
data = pd.DataFrame(result['data'])
data = data.dropna()
data = data[['總資本支出成長率', 'P/B', '現金比率', 'P/S', '總投入資本營運報酬率', '普通股權益報酬率', '總債務/總資產', '毛利率', '獲利率']].tail(30)
data = data.drop(data[data['總資本支出成長率'] == "nodata"].index)
print(data)



# CRUD Practice

# query1 : 基本搜尋
# data = coll.find()
# for d in data:
#     print(d['name'])

# query2 : regex, name contains ASUS
# data = coll.find({'name': {'$regex': '.*ASUS.*'}})
# for d in data:
#     print(d['name'])

# query3 : comparison operator
# data = coll.find({'price': {'$gt' : 3000}})
# for d in data:
#     print(d['name'], d['price'])

# query4 : and comparison operator with list, asus and price greater than 3000
# data = coll.find({'$and': [{'name': {'$regex': '.*ASUS.*'}}, {'price': {'$gt': 3000}}]})
# for d in data:
#     print(d['name'], d['price'])


# update1 : format for update data

# data = coll.find_one({'name': 'ASUS XG35VQ(低藍光+不閃屏)'})
# print(data['name'], data['price'])
#
# coll.update_one({'name': 'ASUS XG35VQ(低藍光+不閃屏)'}, {'$set': {'price': 8000}})
#
# data = coll.find_one({'name': 'ASUS XG35VQ(低藍光+不閃屏)'})
# print(data['name'], data['price'])


# update2 : insert if not exist using upsert
# coll.update_one({'name': 'APPLE'}, {'$set': {'name': 'APPLE'}}, upsert= True)

# delete : delete data
# coll.delete_one({'name': 'APPLE'})
