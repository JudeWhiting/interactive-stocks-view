from dateutil.relativedelta import relativedelta
from datetime import datetime

def date_x_months_ago(today: datetime, months_ago: int, to_datetime: bool=False) -> datetime:
    if to_datetime:
        return today - relativedelta(months=months_ago)
    else:
        return (today - relativedelta(months=months_ago)).strftime('%m-%Y')

def get_api_key():
    f = open("apikey.txt", "r")
    return f.readline().strip()
