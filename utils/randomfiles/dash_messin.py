from dash import Dash, html, dash_table
import pandas as pd
import requests


def build_table():
    url = 'https://api.polygon.io/v3/reference/tickers?ticker=AAPL&market=stocks&active=true&order=asc&limit=100&sort=ticker&apiKey=1pNFJbbF9avSxxJhk8w83zLmF565kTpl'

    response = requests.get(url)
    print(response.text)
    df = pd.DataFrame([response])

    return df



def build_app(df):
    app = Dash()
    app.layout = [html.Div(children='Hello World'),
                  dash_table.DataTable(data=df.to_dict('records'), page_size=10),]

    app.run(debug=True)

if __name__ == '__main__':
    df = build_table()
    #build_app(df)
    print(df.loc[0])
