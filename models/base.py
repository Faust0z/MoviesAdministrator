from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DB_URI

Base = declarative_base()
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
