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
        return (session.query(Movie)
                .options(joinedload(Movie.director))
                .options(joinedload(Movie.actors))
                .options(joinedload(Movie.genres))
                .all())
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []
    finally:
        session.close()


def update_movie(updated_movie: Movie):
    session = get_session()
    try:
        movie = (session.get(Movie, updated_movie.movie_id)
                 .options(joinedload(Movie.director))
                 .options(joinedload(Movie.actors))
                 .options(joinedload(Movie.genres)))

        if movie:
            movie.title = updated_movie.title
            movie.release_year = updated_movie.release_year
            movie.runtime = updated_movie.runtime
            movie.director_id = updated_movie.director_id
            movie.actors = [session.merge(actor) for actor in updated_movie.actors]
            movie.genres = [session.merge(genre) for genre in updated_movie.genres]
            session.commit()
    except Exception as e:
        print(f"Error updating movie: {e}")
        return []
    finally:
        session.close()


def delete_movie(deleted_movie: Movie):
    session = get_session()
    try:
        movie = session.get(Movie, deleted_movie.movie_id)
        if movie:
            session.delete(movie)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error deleting movie: {e}")
    finally:
        session.close()
