from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config.settings import DB_URI

engine = create_engine(DB_URI, echo=False, future=True)
SessionFactory = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    def __repr__(self):
        return f"<{self.__class__.__name__}({self.__dict__})>"


def get_session():
    return SessionFactory()
