from sqlmodel import Session
#from database.models import AggregateBar
#from database.database import ENGINE
from models import AggregateBar
from database import ENGINE

class AggregateBarService:
    @staticmethod
    def insert_row(row: AggregateBar):
        with Session(ENGINE) as session:
            session.add(row)
            session.commit()
            session.refresh(row)
            return row

    @staticmethod
    def get_all():
        with Session(ENGINE) as session:
            return session.exec("SELECT * FROM aggregate_bar").all()
