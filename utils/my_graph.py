import dash
from dash import dcc, html
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output


def price_path(m, T, sigma, s0, r):
    u = np.exp(sigma * np.sqrt(T / m))
    d = 1 / u
    q = (np.exp(sigma * T / m) - d) / (u - d)

    up_or_down = np.where(np.random.rand(m) < q, u, d)
    up_or_down[0] = 1.
    prices = s0 * np.cumprod(up_or_down)

    return prices

rd_walk = price_path(m=3000,T=3,sigma=0.25,s0=50,r=0.05)

app = dash.Dash(__name__)

# Define the layout of the webpage
app.layout = html.Div([
    html.H1("Interactive Stock Graph"),
    dcc.Slider(
        id='range-slider',
        min=500,
        max=3000,
        step=100,
        value=500,
        #marks={i: f'{i}' for i in range(1, 11)},
        updatemode='drag'
    ),
    dcc.Graph(id='stock-graph')
])


# Define the callback to update the graph based on slider value
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('range-slider', 'value')]
)

#def update_graph(range_slider):


def update_plot(frequency):
    # Create x data

    x = [i for i in range(len(rd_walk))]
    x = x[-frequency:]
    # Create y data based on the frequency
    y = rd_walk[-frequency:]

    tick_vals = [i for i in x[-30::-30]]

    # Create the plotly figure
    figure = {
        'data': [
            go.Scatter(x=x, y=y, mode='lines', name=f'Stock Graph', hoverinfo='skip')
        ],
        'layout': go.Layout(
            title=f'Interactive Historical Stock View',
            xaxis= {'title': 'Time',
                    'tickvals': tick_vals,
                    'ticktext': [f'{i} months ago' for i in range(1, len(tick_vals))],
                    },
            yaxis={'title': 'Stock Price (£)',},
            template='plotly_dark'
        )
    }
    return figure

app.run(debug=True)

