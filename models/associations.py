from sqlalchemy import Column, Integer, ForeignKey, Table
from models.base import Base

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
