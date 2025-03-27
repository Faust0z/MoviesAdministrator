from sqlalchemy.orm import joinedload

from models.base import get_session
from models.genre import Genre

def add_genre(new_genre: Genre):
    session = get_session()
    try:
        session.add(new_genre)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding genre: {e}")
    finally:
        session.close()


def get_genres():
    session = get_session()
    try:
        return session.query(Genre).all()
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return []
    finally:
        session.close()


def update_genre(updated_genre: Genre):
    session = get_session()
    try:
        genre  = (session.get(Genre, updated_genre.genre_id)
                  .options(joinedload(Genre.movies)))

        if genre:
            genre.name = updated_genre.name
            genre.movies = [session.merge(movie) for movie in updated_genre.movies]
            session.commit()
    except Exception as e:
        print(f"Error updating genre: {e}")
        return []
    finally:
        session.close()


def delete_genre(deleted_genre: Genre):
    session = get_session()
    try:
        director = session.get(Genre, deleted_genre.director_id)
        if director:
            session.delete(director)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error deleting director: {e}")
    finally:
        session.close()