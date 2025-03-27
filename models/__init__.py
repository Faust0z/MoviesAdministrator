from models.base import Base, engine
from models.movie import Movie
from models.actor import Actor
from models.director import Director
from models.genre import Genre
from models.associations import movies_have_genres, movies_have_actors

Base.metadata.create_all(engine) # Will create ALL tables IF they don't exist