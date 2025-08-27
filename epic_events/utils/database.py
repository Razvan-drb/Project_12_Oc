from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from epic_events.models.base import Base
import os


def get_db_url():

    return os.getenv('DATABASE_URL', 'sqlite:///epic_events.db')

engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()