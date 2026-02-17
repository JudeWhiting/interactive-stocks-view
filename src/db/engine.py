from pathlib import Path
from sqlmodel import create_engine

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "interactive-stocks-view" / "database"
DATA_DIR.mkdir(exist_ok=True)
sqlite_url = f"sqlite:///{DATA_DIR / 'interactive_stocks_view.db'}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
)
