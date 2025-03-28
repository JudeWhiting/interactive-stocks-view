from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import polygon
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import deque

def date_x_months_ago(today: datetime, months_ago: int, to_datetime: bool=False) -> datetime:
    if to_datetime:
        return today - relativedelta(months=months_ago)
    else:
        return (today - relativedelta(months=months_ago)).strftime('%m-%Y')

date_from: datetime
date_to: datetime
date_today = datetime.today()

data_table: pd.DataFrame = pd.DataFrame()

STOCKS_CLIENT: polygon.StocksClient = polygon.StocksClient("1pNFJbbF9avSxxJhk8w83zLmF565kTpl")
DEFAULT_TICKER: str = "AAPL"
COLOR_MAP: dict = {"PRICE": "grey", f"SMA{100}": "black", f"EMA{104}": "blue", f"EMA{48}": "red"}



app = Dash(__name__)
app.layout = html.Div([
    html.Div(dcc.Input(id="ticker-text-box", type="text", placeholder="Enter Ticker ID")),
    dcc.Slider(
        id="sma_slider",
        min=10,
        max=200,
        step=10,
        value=100,
    ),
    dcc.Slider(
        id="ema_slider",
        min=12,
        max=60,
        step=12,
        value=48
    ),
    html.Button(id="send-query-button", n_clicks=0, children="Send Query"),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        [f"SMA{100}", "EMA"],
        [f"SMA{100}", "EMA"],
        id="checklist",
    ),
    dcc.Slider(
        id="date_slider",
        min=0,
        max=18,
        step=1,
        value=0,
        marks={
            0: date_x_months_ago(date_today, 18),
            6: date_x_months_ago(date_today, 12),
            12: date_x_months_ago(date_today, 6),
            18: "This Month",
        },
    ),
])
# @app.callback(
#     Output("graph", "figure"),
#     Input("ticker-text-box", "value"),
#     Input("checklist", "value"),
#     Input("date_slider", "value"),
#     Input("sma_slider", "value"),
#     Input("ema_slider", "value"),
#     prevent_initial_call=True
# )
# def update_plot(ticker: str, checklist: list, months_slider: int, sma_slider: int, ema_slider: int) -> px.line:
#     global prev_ticker
#     global stock_data
#     months_slider = 19 - months_slider
#     ticker = format_ticker(ticker)
#     if ticker != prev_ticker:
#         try:
#             sma = get_format_sma(ticker)
#             global date_from, date_to
#             date_from, date_to = get_daterange(sma)
#             price = get_format_price(ticker)
#             ema_short = get_format_ema(ticker, window_size=ema_short_window)
#             ema_long = get_format_ema(ticker, window_size=ema_long_window)
#
#             stock_data = pd.concat([sma, ema_short, ema_long, price])
#         except: # change excepts make more
#             if recent_status == "ERROR":
#                 error_msg = "API called too many times, please wait before sending another request."
#             else:
#                 error_msg = "Invalid ticker ID."
#             return px.line(pd.DataFrame(), title=error_msg)
#
#         prev_ticker = str(ticker)
#
#
#     plot_data = pd.DataFrame()
#
#     if "EMA" in checklist:
#         checklist.remove("EMA")
#         checklist.append(f"EMA{ema_long_window}")
#         checklist.append(f"EMA{ema_short_window}")
#     checklist.reverse()
#     checklist.append("PRICE")
#
#
#     for i in checklist:
#         plot_data = pd.concat([stock_data.query(f"type == '{i}'"), plot_data])
#
#     plot_data = plot_data[plot_data["date"] >= date_x_months_ago(date_to, months_slider, to_datetime=True)]
#     print(plot_data)
#     print("XXXXXXXXXX")
#     print(date_today)
#     print("XXXXXXXXX")
#     print(date_x_months_ago(date_from, months_slider, to_datetime=True))
#
#     fig = px.line(plot_data, x="date", y="value", title=f"${ticker} Stock Data", color_discrete_map=COLOR_MAP, color="type",
#                   labels={"date": "Date", "value": "Value", "type": "Legend"})
#     fig.update_layout(yaxis_tickformat="$")
#     return fig

@app.callback(
    Output("graph", "figure", allow_duplicate=True),
    Input("send-query-button", "n_clicks"),
    State("ticker-text-box", "value"),
    State("sma_slider", "value"),
    State("ema_slider", "value"),
    State("checklist", "value"), #
    State("date_slider", "value"),
    prevent_initial_call=True
)
def get_data(n_clicks, ticker: str, sma_val: int, ema_val: int, graph_checklist: list, months_slider: int) -> pd.DataFrame:
    global data_table
    global date_from, date_to
    ticker = ticker.upper().strip()
    ema_long_val = int((ema_val/12) * 26)
    ema_short_val = int(ema_val)

    sma = get_format_sma(ticker, window_size=sma_val)
    date_from, date_to = get_daterange(sma)
    price = get_format_price(ticker)
    ema_short = get_format_ema(ticker, window_size=ema_short_val)
    ema_long = get_format_ema(ticker, window_size=ema_long_val)
    donchian = calculate_donchian_channel(price, 50)

    data_table = pd.concat([sma, ema_short, ema_long, price, donchian])
    print(data_table)




    return update_plot(graph_checklist, months_slider)

@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
    Input("date_slider", "value"),
    prevent_initial_call=True
)
def update_plot(graph_checklist: list, months_slider: int) -> px.line:
    months_slider = 19 - months_slider
    plot_data = pd.DataFrame()
    if "EMA" in graph_checklist:
        graph_checklist.remove("EMA")
        graph_checklist.append(f"EMA{48}") # needs fixing
        graph_checklist.append(f"EMA{104}")
    graph_checklist.reverse()
    graph_checklist.append("PRICE")
    graph_checklist.append("Donchian Upper")
    graph_checklist.append("Donchian Lower")
    graph_checklist.append("Donchian Avg")
    for i in graph_checklist:
        plot_data = pd.concat([data_table.query(f"type == '{i}'"), plot_data]) # this can be simplified

    plot_data = plot_data[plot_data["date"] >= date_x_months_ago(date_to, months_slider, to_datetime=True)]

    fig = px.line(plot_data, x="date", y="value", title="Stock Data", color_discrete_map=COLOR_MAP,
                  color="type",
                  labels={"date": "Date", "value": "Value", "type": "Legend"})
    fig.update_layout(yaxis_tickformat="$")
    return fig


def get_format_sma(ticker: str, window_size: int) -> pd.DataFrame:
    stocks = STOCKS_CLIENT.get_sma(ticker, window_size=window_size)
    #global recent_status
    #recent_status = stocks["status"]
    stocks = stocks["results"]["values"]
    df = pd.DataFrame(stocks)
    df["type"] = f"SMA{window_size}"
    df = df.rename(columns={"timestamp": "date"})
    df["date"] = df["date"].apply(lambda unixtimestamp: datetime.date(datetime.fromtimestamp(unixtimestamp/1000)))
    return df

def get_format_ema(ticker: str, window_size: int) -> pd.DataFrame:
    stocks = STOCKS_CLIENT.get_ema(ticker, window_size=window_size, timestamp_gte=date_from)
    #global recent_status
    #recent_status = stocks["status"]
    stocks = stocks["results"]["values"]
    df = pd.DataFrame(stocks)
    df["type"] = f"EMA{window_size}"
    df = df.rename(columns={"timestamp": "date"})
    df["date"] = df["date"].apply(lambda unixtimestamp: datetime.date(datetime.fromtimestamp(unixtimestamp/1000)))
    return df

def get_format_price(ticker: str) -> pd.DataFrame:
    stocks = STOCKS_CLIENT.get_aggregate_bars(ticker, date_from, date_to)
    #global recent_status
    #recent_status = stocks["status"]
    stocks = stocks["results"]
    df = pd.DataFrame(stocks)
    df = df[["c", "t"]]
    df["type"] = "PRICE"
    df = df.rename(columns={"t": "date", "c": "value"})
    df["date"] = df["date"].apply(lambda unixtimestamp: datetime.date(datetime.fromtimestamp(unixtimestamp / 1000)))
    return df

def calculate_donchian_channel(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    # maybe change code outside of this so the dataframe is ordered earliest to latest date
    print(df.columns)
    print(df)
    last_n_values = deque(maxlen=window_size)
    max_vals = []
    min_vals = []
    avg_vals = []
    dates = []

    if df.iloc[-1]["date"] < df.iloc[0]["date"]:
        # checks if the dates are the right way around (earlier dates should be at top of df)
        df = df[::-1]

    for row in df.itertuples():
        last_n_values.append(row[1])
        dates.append(row[2])
        max_val = max(last_n_values)
        min_val = min(last_n_values)
        avg_val = (max_val + min_val) / 2

        max_vals.append(max_val)
        min_vals.append(min_val)
        avg_vals.append(avg_val)

    donchian_max = pd.DataFrame({"date": dates, "value": max_vals, "type": "Donchian Upper" })
    donchian_min = pd.DataFrame({"date": dates, "value": min_vals, "type": "Donchian Lower" })
    donchian_avg = pd.DataFrame({"date": dates, "value": avg_vals, "type": "Donchian Avg"})
    return pd.concat([donchian_max, donchian_min, donchian_avg])



def get_daterange(df: pd.DataFrame):
    return df["date"].min(), df["date"].max()


if __name__ == "__main__":
    # sma = get_format_sma("AAPL", 50)
    # calculate_donchian_channel(sma, 20)
    app.run(debug=True)


# figure optimal way to structure callbacks to plot multiple graphs of same stock
# make new column which labels what plot the values belong to and then concat everything together
# https://dash.plotly.com/basic-callbacks - for dash callbacks
# https://plotly.com/python/plotly-fundamentals/ - for plotly graphing
# https://polygon.readthedocs.io/en/latest/Stocks.html - for getting stock data
# IMPORTANT TO DO
# sort out datetime global vars
# make a slider for donchian channel
# sort out sma and ema window vars and make sure the ema and sma sliders work
# make checkbox work better