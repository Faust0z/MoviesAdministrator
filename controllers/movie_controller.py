from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, Session

from models.actor import Actor
from models.base import get_session
from models.director import Director
from models.genre import Genre
from models.movie import Movie


def add_movie(new_movie: Movie, session: Session):
    try:
        with session.begin():
            session.add(new_movie)
    except Exception as e:
        print(f"Error adding movie: {e}")


def get_movies(session: Session = None):
    session = session if session else get_session()
    try:
        return (session.query(Movie)
                .options(joinedload(Movie.director))
                .options(joinedload(Movie.actors))
                .options(joinedload(Movie.genres))
                .all())
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []


def get_movies_dict(filter_value: str = None, session: Session = None):
    session = session if session else get_session()
    try:
        filters = []
        if filter_value:
            like_pattern = f"%{filter_value}%"
            filters.append(Movie.title.ilike(like_pattern))
            filters.append(Movie.runtime.ilike(like_pattern))
            filters.append(Movie.release_year.ilike(like_pattern))
            filters.append(Director.name.ilike(like_pattern))
            filters.append(Actor.name.ilike(like_pattern))
            filters.append(Genre.name.ilike(like_pattern))

        stmt = (
            select(Movie)
            .join(Movie.director)
            .outerjoin(Movie.actors)
            .outerjoin(Movie.genres)
            .options(joinedload(Movie.director))
            .options(joinedload(Movie.actors))
            .options(joinedload(Movie.genres))
        )

        if filters:
            stmt = stmt.where(or_(*filters))

        with session.begin():
            movies = session.execute(stmt).unique().scalars().all()
            return [{
                "ID": movie.movie_id,
                "Title": movie.title,
                "Release Year": movie.release_year,
                "Runtime": movie.runtime,
                "Director name": movie.director.name if movie.director else "",
                "Actors": ", ".join(actor.name for actor in movie.actors),
                "Genres": ", ".join(genre.name for genre in movie.genres)
            } for movie in movies
            ]
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []


def update_movie(updated_movie: Movie):
    session = get_session()
    try:
        with session.begin():
            movie = (session.query(Movie)
                     .filter_by(movie_id=updated_movie.movie_id)
                     .options(joinedload(Movie.director))
                     .options(joinedload(Movie.actors))
                     .options(joinedload(Movie.genres))
                     .first())

            if movie:
                movie.title = updated_movie.title
                movie.release_year = updated_movie.release_year
                movie.runtime = updated_movie.runtime
                movie.director_id = updated_movie.director_id
                movie.actors = [session.merge(actor) for actor in updated_movie.actors]
                movie.genres = [session.merge(genre) for genre in updated_movie.genres]

    except Exception as e:
        print(f"Error updating movie: {e}")
        return []


def delete_movie(deleted_movie: Movie):
    session = get_session()
    try:
        with session.begin():
            movie = session.get(Movie, deleted_movie.movie_id)
            if movie:
                session.delete(movie)
    except Exception as e:
        print(f"Error deleting movie: {e}")
