from sqlmodel import Field, SQLModel
from typing import Optional

class AggregateBar(SQLModel, table=True):
    __tablename__ = "aggregate_bar"

    id: Optional[int] = Field(default=None, primary_key=True)  # auto-increment
    ticker: str = Field(nullable=False)
    datetime: str = Field(nullable=False)
    volume: Optional[int] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume_weighted_average_price: Optional[float] = None

class DonchianChannel(SQLModel, table=True):
    __tablename__ = "donchian_channel"

    id: Optional[int] = Field(default=None, primary_key=True)
    aggregate_bar_id: Optional[int] = Field(default=None)
    ticker: str = Field(nullable=False)
    datetime: str = Field(nullable=False)
    upper: Optional[float] = None
    lower: Optional[float] = None
    average: Optional[float] = None