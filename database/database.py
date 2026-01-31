from sqlmodel import create_engine

def initialise_engine():
    db_path = "interactive-stocks-view.db"
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(
        db_url,
        echo=True,  # set False in prod
    )
    engine = create_engine(db_url, echo=True)
    return(engine)

ENGINE = initialise_engine()


