from sqlalchemy.orm import joinedload

from models.base import get_session
from models.movie import Movie

def add_movie(new_movie: Movie):
    session = get_session()
    try:
        session.add(new_movie)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding movie: {e}")
    finally:
        session.close()

def get_movies():
    session = get_session()
    try:
        return session.query(Movie).options(joinedload(Movie.director)).options(joinedload(Movie.actors)).options(joinedload(Movie.genres)).all()
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []
    finally:
        session.close()


def update_movie(movie_id, updated_data):
    session = get_session()
    movie = session.query(Movie).filter_by(movie_id=movie_id).first()

    if movie:
        movie.title = updated_data["Title"]
        movie.release_year = updated_data["Release Year"]
        movie.runtime = updated_data["Runtime"]
        session.commit()

    session.close()


def delete_movie(movie_id):
    session = get_session()
    try:
        movie = session.get(Movie, movie_id)
        if movie:
            session.delete(movie)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error deleting movie: {e}")
    finally:
        session.close()