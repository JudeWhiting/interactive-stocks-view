# import plotly.express as px
#
# df = px.data.gapminder().query("continent=='Oceania'")
# fig = px.line(df, x="year", y="lifeExp", color='country')
# print(df)
# fig.show()

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import polygon
import pandas as pd
from datetime import datetime

stocks_client = polygon.StocksClient("1pNFJbbF9avSxxJhk8w83zLmF565kTpl")
default_ticker = "AAPL"

app = Dash(__name__)
app.layout = html.Div([
    html.H4("Stock Graph"),
    dcc.Input(id="ticker-text-box", type="text", placeholder="Enter Ticker", debounce=True),
    dcc.Graph(id="graph"),
])
@app.callback(
    Output("graph", "figure"),
    Input("ticker-text-box", "value"))
def update_plot(input_value: str) -> px.line:
    input_value = format_ticker(input_value)
    stock_data1 = get_format_sma(input_value)
    stock_data2 = test()
    stock_data = pd.concat([stock_data1, stock_data2])
    print(stock_data)
    fig = px.line(stock_data, x="timestamp", y="value", color='ticker')
    return fig

def get_format_sma(ticker: str) -> pd.DataFrame:
    stocks = stocks_client.get_sma(ticker)
    stocks = stocks["results"]["values"]
    df = pd.DataFrame(stocks)
    df['ticker'] = ticker
    df["timestamp"] = df["timestamp"].apply(lambda unixtimestamp: datetime.fromtimestamp(unixtimestamp/1000))
    return df

def test():
    stocks = stocks_client.get_sma("TSLA")
    stocks = stocks["results"]["values"]
    df = pd.DataFrame(stocks)
    df['ticker'] = 'TSLA'
    df["timestamp"] = df["timestamp"].apply(lambda unixtimestamp: datetime.fromtimestamp(unixtimestamp / 1000))
    return df

def format_ticker(ticker: str) -> str:
    return ticker.upper().strip() if ticker else default_ticker

if __name__ == "__main__":
    app.run(debug=True)
