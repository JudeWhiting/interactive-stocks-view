from datetime import datetime
from models import AggregateBar
from aggregate_bar_service import AggregateBarService

if __name__ == "__main__":


    new_row = AggregateBar(
        ticker="AAPL",
        datetime=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        volume=1000,
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume_weighted_average_price=152.5
    )

    row = AggregateBarService.insert_row(new_row)
    print(row)
