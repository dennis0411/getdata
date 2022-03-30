import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pymongo import MongoClient
from utils import Header, make_dash_table
from warnings import simplefilter
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
import yfinance as yf  # Yahoo Finance python API
import pandas as pd
import ffn
import plotly.express as px

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





if __name__ == "__main__":
    # mongodb connection
    CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
    db = client.getdata
    collection = db.bb
    symbol = collection.find_one(filter={'Ticker': 'AAPL'})
    data = collection.find(filter={'Sector': symbol['Sector']})

    data1 = []
    data2 = []
    data3 = []
    for a in data:
        data1.append(a[dropdown2])
        data2.append(a[dropdown3])
        data3.append(a['Ticker'])
    result = pd.DataFrame(zip(data1, data2, data3), columns=[dropdown2, dropdown3, 'Ticker'])
    result.sort_values(by=dropdown2)


    fig = px.scatter(result, x=result[dropdown2], y=result[dropdown3], hover_name='Ticker', log_x=True)
    fig.update_layout(autotypenumbers='convert types')

    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    # run server
    app.run_server(debug=True)