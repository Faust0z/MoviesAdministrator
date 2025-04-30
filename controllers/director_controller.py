from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, Session

from models.base import get_session
from models.director import Director
from models.movie import Movie


def add_director(new_director: Director, session: Session):
    try:
        with session.begin():
            session.add(new_director)

    except Exception as e:
        print(f"Error adding director: {e}")


def get_directors(session: Session = None):
    session = session or get_session()
    try:
        stmt = select(Director)
        return session.scalars(stmt).unique().all()

    except Exception as e:
        print(f"Error fetching directors: {e}")
        return []


def get_directors_dict(filter_value: str = None, session: Session = None):
    session = session or get_session()
    try:
        like_pattern = f"%{filter_value}%"
        filters = [
            field.ilike(like_pattern)
            for field in [Movie.title, Director.name, Director.sex, Director.birth_year]
        ] if filter_value else []

        stmt = (
            select(Director).distinct()
            .outerjoin(Director.movies)
            .options(joinedload(Director.movies))
        )

        if filters:
            stmt = stmt.where(or_(*filters))

        with session.begin():
            directors = session.execute(stmt).unique().scalars().all()
            return [director.to_dict() for director in directors]

    except Exception as e:
        print(f"Error fetching directors: {e}")
        return []


def update_director(updated_director: Director):
    session = get_session()
    try:
        with session.begin():
            director = session.get(Director, updated_director.director_id)

            if director:
                director.name = updated_director.name
                director.birth_year = updated_director.birth_year
                director.sex = updated_director.sex

    except Exception as e:
        print(f"Error updating director: {e}")
        return []


def delete_director(deleted_director: Director):
    session = get_session()
    try:
        with session.begin():
            director = session.get(Director, deleted_director.director_id)
            if director:
                session.delete(director)

    except Exception as e:
        print(f"Error deleting director: {e}")
