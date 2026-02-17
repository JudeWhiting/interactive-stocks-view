from massive import RESTClient
from db.query.aggregate_bar_query_service import AggregateBarQueryService


def get_api_key():
    f = open("src/api/apikey.txt", "r")
    return f.readline().strip()


def get_format_price(ticker, date_from, date_to):
    client = RESTClient(get_api_key())
    aggs = []

    try:
        for a in client.list_aggs(
            ticker,
            1,
            "day",
            date_from,
            date_to,
            adjusted="true",
            sort="asc",
            limit=120
        ):
            my_row = AggregateBarQueryService.to_sqlmodel(a, ticker)
            AggregateBarQueryService.insert_row(my_row)

    except Exception as e:
        print(e)
