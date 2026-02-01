from dash import Dash, dcc, html
from utils import misc

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
                0: misc.date_x_months_ago(24),
                6: misc.date_x_months_ago(18),
                12: misc.date_x_months_ago(12),
                18: misc.date_x_months_ago(6),
                24: "This Month",
            },
        ),
        style={"width": "50%"},
    ),

    dcc.Store(id="data-table"),
],
)