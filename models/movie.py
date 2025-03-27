from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.associations import movies_have_actors, movies_have_genres
from models.base import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    release_year = Column(Integer, nullable=False)
    runtime = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.director_id"))

    director = relationship("Director", back_populates="movies")
    actors = relationship("Actor", secondary=movies_have_actors, back_populates="movies")
    genres = relationship("Genre", secondary=movies_have_genres, back_populates="movies")

    def __init__(self, title, release_year, runtime, director_id):
        self.title = title
        self.release_year = release_year
        self.runtime = runtime
        self.director_id = director_id

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(title={repr(self.title)},"
                f" release_year={repr(self.release_year)},"
                f" runtime={repr(self.runtime)},"
                f" director_id={repr(self.director_id)})"
                )