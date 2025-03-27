from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.associations import movies_have_genres
from models.base import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    movies = relationship("Movie", secondary=movies_have_genres, back_populates="genres")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)})"
                )
