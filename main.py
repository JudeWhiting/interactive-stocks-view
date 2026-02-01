from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
from core.services.aggregate_bar_query_service import AggregateBarQueryService
from layout import *
from api import api

from scripts import delete_all_db_data



DATEFROM = "2025-11-03"
DATETO = "2025-11-28"

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
def update_plot(graph_checklist: list, months_slider: int, raw_data) -> px.line:
    fig = px.line(
        raw_data, x="datetime", y="close", title="Stock Data", color_discrete_map=COLOR_MAP,
        #color="type",
        #labels={"t": "Date", "c": "Value", "type": "Legend"},
    )
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
    app.run(debug=True)
