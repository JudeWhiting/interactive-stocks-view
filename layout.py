from dash import Dash, dcc, html
from datetime import datetime
from dateutil.relativedelta import relativedelta

def date_x_months_ago(months_ago: int, to_datetime: bool=False) -> datetime:
    today = datetime.today()
    if to_datetime:
        return today - relativedelta(months=months_ago)
    else:
        return (today - relativedelta(months=months_ago)).strftime('%m-%Y')

app = Dash(__name__)
app.layout = html.Div([

    html.Div(dcc.Input(id="ticker-text-box", type="text", placeholder="Enter Ticker ID", value="")),

    html.Button(id="send-query-button", n_clicks=0, children="Send Query"),

    dcc.Graph(id="graph"),

    html.Div(
        dcc.Checklist(
            ["Simple Moving Average", "Donchian Channel"],
            [],
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
            min=1,
            max=12,
            step=1,
            value=12,
            marks={
                1: "This Month",
                3: "Three Months",
                6: "Half-Year",
                9: "Nine Months",
                12: "This Year",
            },
        ),
        style={"width": "50%"},
    ),

    dcc.Store(id="data-table"),
],
)