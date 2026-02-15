from massive import RESTClient
from db.query.aggregate_bar_query_service import AggregateBarQueryService


def get_api_key():
    f = open("src/api/apikey.txt", "r")
    return f.readline().strip()

CLIENT = RESTClient(get_api_key())

from datetime import date
from dateutil.relativedelta import relativedelta

DATETO = date.today()
DATEFROM = DATETO - relativedelta(years=1)


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
        my_row = AggregateBarQueryService.to_sqlmodel(a, ticker)
        AggregateBarQueryService.insert_row(my_row)