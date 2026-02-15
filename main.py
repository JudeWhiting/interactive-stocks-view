from dash import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from db.query.aggregate_bar_query_service import AggregateBarQueryService
from layout import *
from api import api
from services import calculate_graph
from datetime import date
from dateutil.relativedelta import relativedelta

DATETO = date.today()
DATEFROM = DATETO - relativedelta(years=1)

COLOR_MAP: dict = {"PRICE": "grey",}







@app.callback(
    Output("data-table", "data", allow_duplicate=True),
    Input("send-query-button", "n_clicks"),
    State("ticker-text-box", "value"),
    State("checklist", "value"),
    State("sma-slider", "value"),
    State("donchian-slider", "value"),
    State("date-slider", "value"),
    prevent_initial_call=True
)
def get_data(_, ticker: str, graph_checklist: list, sma_window: int, donchian_window: int, months_slider: int):
    ticker = ticker.upper().strip()
    api.get_format_price(ticker)
    return AggregateBarQueryService.read_by_date(DATEFROM, DATETO)



@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
    Input("date-slider", "value"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_plot(graph_checklist: list, months_slider: int, raw_data):
    fig = go.Figure()
    donchian = calculate_graph.donchian_channel(raw_data, 50)
    sma = calculate_graph.simple_moving_average(raw_data, 50)

    fig.add_trace(go.Scatter(x=[item["datetime"] for item in raw_data], y=[item["close"] for item in raw_data], mode="lines", name="price"))
    fig.add_trace(go.Scatter(x=[item["datetime"] for item in raw_data], y=donchian["max"], mode="lines", name="donchian_max"))
    fig.add_trace(go.Scatter(x=[item["datetime"] for item in raw_data], y=donchian["min"], mode="lines", name="donchian_min"))
    fig.add_trace(go.Scatter(x=[item["datetime"] for item in raw_data], y=donchian["avg"], mode="lines", name="donchian_avg"))
    fig.add_trace(go.Scatter(x=[item["datetime"] for item in raw_data], y=sma, mode="lines", name="sma"))


    fig.update_layout(yaxis_tickformat="$")

    return fig



@app.callback(
    Output("data-table", "data", allow_duplicate=True),
    Input("donchian-slider", "value"),
    State("data-table", "data"),
    prevent_initial_call=True
)
def update_donchian(donchian_window: int, raw_data: str) -> str:
    mydata = pd.read_json(raw_data, orient="records")
    mydata = mydata[~((mydata["type"]=="Donchian Upper") | (mydata["type"]=="Donchian Lower") | (mydata["type"]=="Donchian Avg"))]
    donchian = calculate_graph.donchian_channel(mydata, donchian_window)
    mydata = pd.concat([mydata, donchian])

    return mydata.to_json(orient="records")



@app.callback(
    Output("data-table", "data", allow_duplicate=True),
    Input("sma-slider", "value"),
    State("data-table", "data"),
    prevent_initial_call=True
)
def update_sma(sma_window: int, raw_data: str) -> str:
    mydata = pd.read_json(raw_data, orient="records")
    mydata = mydata[mydata["type"] != "Simple Moving Average"]
    sma = calculate_graph.simple_moving_average(mydata, sma_window)
    mydata = pd.concat([mydata, sma])

    return mydata.to_json(orient="records")



if __name__ == "__main__":
    AggregateBarQueryService.delete_all()
    app.run(debug=True)
