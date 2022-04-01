import datetime
from dash import Dash, html, Input, Output, dash_table
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
from datetime import date

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
    app = Dash(__name__)

    df = []

    app.layout = html.Div([
        html.H4('Simple interactive table'),
        html.P(id='table_out'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i}
                     for i in df.columns],
            data=df.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender")
        ),
    ])


    @app.callback(
        Output('table_out', 'children'),
        Input('table', 'active_cell'))
    def update_graphs(active_cell):
        if active_cell:
            cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
            return f"Data: \"{cell_data}\" from table cell: {active_cell}"
        return "Click the table"


    app.run_server(debug=True)


