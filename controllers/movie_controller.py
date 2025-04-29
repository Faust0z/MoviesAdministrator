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
    session = session or get_session()
    try:
        stmt = (select(Movie)
                .options(joinedload(Movie.director))
                .options(joinedload(Movie.actors))
                .options(joinedload(Movie.genres))
                )
        return session.scalars(stmt).unique().all()
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []


def get_movies_dict(filter_value: str = None, session: Session = None):
    session = session or get_session()
    try:
        like_pattern = f"%{filter_value}%"
        filters = [
            field.ilike(like_pattern)
            for field in [Movie.title, Movie.runtime, Movie.release_year, Director.name, Actor.name, Genre.name]
        ] if filter_value else []

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
            return [movie.to_dict() for movie in movies]
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []


def update_movie(updated_movie: Movie):
    session = get_session()
    try:
        with session.begin():
            stmt = (select(Movie)
                    .options(joinedload(Movie.director))
                    .options(joinedload(Movie.actors))
                    .options(joinedload(Movie.genres))
                    )
            movie = session.execute(stmt)

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
