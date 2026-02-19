from dash import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from db.query.aggregate_bar_query_service import AggregateBarQueryService
from db import engine
from layout import *
from api import api
from services import calculate_graph
from datetime import date
from dateutil.relativedelta import relativedelta



@app.callback(
    Output("data-table", "data", allow_duplicate=True),
    Input("send-query-button", "n_clicks"),
    State("ticker-text-box", "value"),
    prevent_initial_call=True)
def get_data(_, ticker):
    ticker = ticker.upper().strip()

    if AggregateBarQueryService.is_missing_ticker(engine, ticker):
        api.get_format_price(engine, ticker, DATEFROM, DATETO)
    elif date.fromisoformat(AggregateBarQueryService.most_recent(engine, ticker).split(" ")[0]) > DATETO:
        api.get_format_price(engine, ticker, date.fromisoformat(AggregateBarQueryService.most_recent(engine, ticker).split(" ")[0]) + relativedelta(days=1), DATETO)

    return AggregateBarQueryService.read_by_ticker(engine, ticker)



@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
    Input("date-slider", "value"),
    Input("checklist", "value"),
    Input("sma-slider", "value"),
    Input("donchian-slider", "value"),
    Input("data-table", "data"))
def update_plot(graph_checklist: list, months_slider: int, checklist, sma_window, donchian_window, raw_data):
    fig = go.Figure()

    if not raw_data:
        return fig

    dates = [item["datetime"] for item in raw_data if date.fromisoformat(item["datetime"].split(" ")[0]) >= DATETO - relativedelta(months=months_slider)]

    fig.add_trace(go.Scatter(x=dates, y=[item["close"] for item in raw_data][-len(dates):], mode="lines", name="price", line={"color": "blue"}))
    if "Simple Moving Average" in checklist:
        sma = calculate_graph.simple_moving_average(raw_data, sma_window)
        fig.add_trace(go.Scatter(x=dates, y=sma[-len(dates):], mode="lines", name="sma", line={"color": "black"}))
    if "Donchian Channel" in checklist:
        donchian = calculate_graph.donchian_channel(raw_data, donchian_window)
        fig.add_trace(go.Scatter(x=dates, y=donchian["max"][-len(dates):], mode="lines", name="donchian_max", line={"color": "green"}))
        fig.add_trace(go.Scatter(x=dates, y=donchian["avg"][-len(dates):], mode="lines", name="donchian_avg", line={"color": "orange"}))
        fig.add_trace(go.Scatter(x=dates, y=donchian["min"][-len(dates):], mode="lines", name="donchian_min", line={"color": "red"}))

    fig.update_layout(yaxis_tickformat="$")
    return fig


if __name__ == "__main__":
    DATETO = date.today()
    DATEFROM = DATETO - relativedelta(years=1)
    engine = engine.get_engine()
    app.run(debug=True)
