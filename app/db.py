from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///data/ehr.db"

# Engine = spojení s databází
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # důležité pro SQLite ve FastAPI
)

# Session = okno pro práci s databází (CRUD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI-compatible session getter
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
