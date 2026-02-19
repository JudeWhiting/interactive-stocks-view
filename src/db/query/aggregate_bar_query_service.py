from sqlmodel import Session, text, select
from db.models import AggregateBar
from datetime import datetime


class AggregateBarQueryService:

    @staticmethod
    def insert_row(engine, row):
        with Session(engine) as session:
            session.add(row)
            session.commit()
            session.refresh(row)
            return row

    @staticmethod
    def read_all(engine):
        with Session(engine) as session:
            return session.exec(text("SELECT * FROM aggregate_bar")).all()

    @staticmethod
    def delete_all(engine):
        with (Session(engine) as session):
            session.exec(text("DELETE FROM aggregate_bar"))
            session.commit(
            )

    @staticmethod
    def to_sqlmodel(response, ticker):
        return AggregateBar(
            ticker=ticker,
            datetime=datetime.utcfromtimestamp(response.timestamp / 1000),
            volume=response.volume,
            open=response.open,
            high=response.high,
            low=response.low,
            close=response.close,
            volume_weighted_average_price=response.vwap
        )

    @staticmethod
    def read_by_ticker(engine, ticker):
        with Session(engine) as session:
            vals = session.exec(
                    select(AggregateBar).where(
                    AggregateBar.ticker == ticker
            ).order_by(AggregateBar.datetime))
            return [bar.model_dump() for bar in vals]

    @staticmethod
    def is_missing_ticker(engine, ticker):
        with Session(engine) as session:
            statement = select(AggregateBar).where(AggregateBar.ticker == ticker).limit(1)
            result = session.exec(statement).first()
            return result == None

    @staticmethod
    def most_recent(engine, ticker):
        with Session(engine) as session:
            result = session.exec(
                select(AggregateBar.datetime).where(
                    AggregateBar.ticker == ticker
                ).order_by(AggregateBar.datetime.desc())
                .limit(1)
            ).first()
            return result


