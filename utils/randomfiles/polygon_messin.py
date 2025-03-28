import polygon
import pandas as pd
from io import StringIO
from pandas import json_normalize

REFERENCE_CLIENT = polygon.ReferenceClient("1pNFJbbF9avSxxJhk8w83zLmF565kTpl")
TICKERS_LIST = REFERENCE_CLIENT.get_tickers(symbol="BTC")#["results"]
print(TICKERS_LIST)
# df = pd.json_normalize(TICKERS_LIST)
df = pd.read_json(TICKERS_LIST)
print(df)
# df.to_excel('data.xlsx', index=False)
# stocksclient = polygon.StocksClient("1pNFJbbF9avSxxJhk8w83zLmF565kTpl")
# x = stocksclient.get_macd("AAPL",long_window_size=51)
# print(x["status"]) # OK or ERROR
# print(x)
# print(x)
