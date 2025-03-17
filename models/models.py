from sqlalchemy import create_engine, Column, Integer, Date, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

db_url = os.getenv("DB_URI")
engine = create_engine(db_url)

Base = declarative_base()

movies_have_actors = Table(
    "movie_actor",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.actor_id"), primary_key=True)
)

movies_have_genres = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)

class Director(Base):
    __tablename__ = "directors"

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    sex = Column(String(100), nullable=False)

    movies = relationship("Movie", back_populates="director")

    def __init__(self, name, birth_year, sex):
        self.name = name
        self.birth_year = birth_year
        self.sex = sex

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)},"
                f" birth_year={repr(self.birth_year)},"
                f" sex={repr(self.sex)})"
                )

class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    sex = Column(String(10), nullable=False)

    movies = relationship("Movie", secondary=movies_have_actors, back_populates="actors")

    def __init__(self, name, birth_year, sex):
        self.name = name
        self.birth_year = birth_year
        self.sex = sex

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)},"
                f" birth_year={repr(self.birth_year)},"
                f" sex={repr(self.sex)})"
                )

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    movies = relationship("Movie", secondary=movies_have_genres, back_populates="genres")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)})"
                )

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    release_year = Column(Date, nullable=False)
    runtime = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.director_id"))

    director = relationship("Director", back_populates="movies")
    actors = relationship("Actor", secondary=movies_have_actors, back_populates="movies")
    genres = relationship("Genre", secondary=movies_have_genres, back_populates="movies")

    def __init__(self, name, release_year, runtime, director_id):
        self.name = name
        self.release_year = release_year
        self.runtime = runtime
        self.director_id = director_id

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)},"
                f" release_year={repr(self.release_year)},"
                f" runtime={repr(self.runtime)},"
                f" director_id={repr(self.director_id)})"
                )

Base.metadata.create_all(engine)  # Will create ALL tables IF they don't exist
