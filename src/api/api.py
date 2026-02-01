from massive import RESTClient
from utils import misc
from core.services.aggregate_bar_query_service import AggregateBarQueryService

CLIENT = RESTClient(misc.get_api_key())

DATEFROM = "2025-11-03"
DATETO = "2025-11-28"

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