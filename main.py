from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
from massive import RESTClient
import pandas as pd
from datetime import datetime
from utils import calculate_graph, misc
from core.db.engine import engine
from core.services.aggregate_bar_query_service import AggregateBarQueryService
from scripts import delete_all_db_data


date_today = datetime.date(datetime.today())
data_table: pd.DataFrame = pd.DataFrame()

CLIENT = RESTClient(misc.get_api_key())
DEFAULT_TICKER: str = "AAPL"
COLOR_MAP: dict = {"PRICE": "grey",}

DATEFROM = "2025-11-03"
DATETO = "2025-11-28"



app = Dash(__name__)
app.layout = html.Div([

    html.Div(dcc.Input(id="ticker-text-box", type="text", placeholder="Enter Ticker ID")),

    html.Button(id="send-query-button", n_clicks=0, children="Send Query"),

    dcc.Graph(id="graph"),

    html.Div(
        dcc.Checklist(
            ["Simple Moving Average", "Donchian Channel"],
            ["Simple Moving Average", "Donchian Channel"],
            id="checklist",
        ),
    ),

    html.Plaintext("Simple Moving Avg Window:"),

    html.Div(
        dcc.Slider(
            id="sma-slider",
            min=10,
            max=200,
            step=10,
            value=50,
        ),
        style={"width": "50%"}
    ),
    html.Plaintext("Donchian Channel Window:"),

    html.Div(
        dcc.Slider(
            id="donchian-slider",
            min=10,
            max=200,
            step=10,
            value=50,
        ),
        style={"width": "50%"}
    ),

    html.Plaintext("Daterange:"),

    html.Div(
        dcc.Slider(
            id="date-slider",
            min=0,
            max=24,
            step=1,
            value=0,
            marks={
                0: misc.date_x_months_ago(date_today, 24),
                6: misc.date_x_months_ago(date_today, 18),
                12: misc.date_x_months_ago(date_today, 12),
                18: misc.date_x_months_ago(date_today, 6),
                24: "This Month",
            },
        ),
        style={"width": "50%"},
    ),

    dcc.Store(id="data-table"),
],
)
@app.callback(
    # Output("graph", "figure", allow_duplicate=True),
    Output("data-table", "data", allow_duplicate=True),
    Input("send-query-button", "n_clicks"),
    State("ticker-text-box", "value"),
    State("checklist", "value"),
    State("sma-slider", "value"),
    State("donchian-slider", "value"),
    State("date-slider", "value"),
    prevent_initial_call=True
)
def get_data(_, ticker: str, graph_checklist: list, sma_window: int, donchian_window: int, months_slider: int) -> pd.DataFrame:
    # global data_table
    # data_table = pd.DataFrame()

    ticker = ticker.upper().strip()
    get_format_price(ticker)
    #donchian = calculate_graph.donchian_channel(price, donchian_window)
    #sma = calculate_graph.simple_moving_average(price, sma_window)
    # data_table = pd.concat([price, donchian, sma])
    #df = pd.concat([price, donchian, sma])
    # return update_plot(graph_checklist, months_slider)
    return AggregateBarQueryService.read_by_date(DATEFROM, DATETO)


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"),
    Input("date-slider", "value"),
    Input("data-table", "data"),
    prevent_initial_call=True
)
def update_plot(graph_checklist: list, months_slider: int, raw_data) -> px.line:
    """
    months_slider = 25 - months_slider
    df = pd.read_json(raw_data, orient="records")

    graph_checklist.append("PRICE")
    if "Donchian Channel" in graph_checklist:
        graph_checklist.remove("Donchian Channel")
        graph_checklist.append("Donchian Upper")
        graph_checklist.append("Donchian Lower")
        graph_checklist.append("Donchian Avg")

    plot_data = pd.DataFrame()
    for i in graph_checklist:
        # plot_data = pd.concat([data_table.query(f"type == '{i}'"), plot_data])
        plot_data = pd.concat([df.query(f"type == '{i}'"), plot_data])

    plot_data["t"] = plot_data["t"].apply(lambda unixtimestamp: datetime.date(datetime.fromtimestamp(unixtimestamp / 1000)))

    plot_data = plot_data[plot_data["t"] >= misc.date_x_months_ago(date_today, months_slider, to_datetime=True)]
    """
    fig = px.line(
        raw_data, x="datetime", y="close", title="Stock Data", color_discrete_map=COLOR_MAP,
        #color="type",
        #labels={"t": "Date", "c": "Value", "type": "Legend"},
    )
    fig.update_layout(yaxis_tickformat="$")

    return fig

@app.callback( # might be a problem with getting and outputting the data table
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


def get_format_price(ticker: str):
    aggs = []

    for a in CLIENT.list_aggs(
            ticker,
            1,
            "day",
            DATEFROM,
            DATETO,
            adjusted="true",
            sort="asc",
            limit=120,
    ):
        my_row = AggregateBarQueryService.transform_json(a, ticker)
        AggregateBarQueryService.insert_row(my_row)


if __name__ == "__main__":
    app.run(debug=True)
