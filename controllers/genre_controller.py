from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, Session

from models.base import get_session
from models.genre import Genre
from models.movie import Movie


def add_genre(new_genre: Genre, session: Session):
    try:
        with session.begin():
            session.add(new_genre)
    except Exception as e:
        print(f"Error adding genre: {e}")


def get_genres(session: Session = None):
    session = session or get_session()
    try:
        stmt = select(Genre)
        return session.scalars(stmt).unique().all()
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return []


def get_genres_dict(filter_value: str = None, session: Session = None):
    session = session or get_session()
    try:
        like_pattern = f"%{filter_value}%"
        filters = [
            field.ilike(like_pattern)
            for field in [Movie.title, Genre.name]
        ] if filter_value else []

        stmt = (
            select(Genre).distinct()
            .outerjoin(Genre.movies)
            .options(joinedload(Genre.movies))
        )

        if filters:
            stmt = stmt.where(or_(*filters))

        with session.begin():
            genres = session.execute(stmt).unique().scalars().all()
            return [{
                "ID": genre.genre_id,
                "Name": genre.name,
                "Movies": ", ".join(movie.title for movie in genre.movies)
            } for genre in genres
            ]
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return []


def update_genre(updated_genre: Genre):
    session = get_session()
    try:
        with session.begin():
            stmt = (
                select(Genre)
                .where(Genre.genre_id == updated_genre.genre_id)
                .options(joinedload(Genre.movies))
            )
            genre = session.execute(stmt)

            if genre:
                genre.name = updated_genre.name
                genre.movies = [session.merge(movie) for movie in updated_genre.movies]
    except Exception as e:
        print(f"Error updating genre: {e}")
        return []


def delete_genre(deleted_genre: Genre):
    session = get_session()
    try:
        with session.begin():
            genre = session.get(Genre, deleted_genre.genre_id)
            if genre:
                session.delete(genre)
    except Exception as e:
        print(f"Error deleting genre: {e}")
