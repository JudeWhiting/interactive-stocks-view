from dateutil.relativedelta import relativedelta
from datetime import datetime

def date_x_months_ago(today: datetime, months_ago: int, to_datetime: bool=False) -> datetime:
    if to_datetime:
        return today - relativedelta(months=months_ago)
    else:
        return (today - relativedelta(months=months_ago)).strftime('%m-%Y')

def get_polygon_key():
    f = open("polygon-key.txt", "r")
    return f.readline().strip()

if __name__ == "__main__":
    print(get_polygon_key())