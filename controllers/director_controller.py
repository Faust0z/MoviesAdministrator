from sqlalchemy.orm import joinedload

from models.base import get_session
from models.director import Director

def add_director(new_director: Director):
    session = get_session()
    try:
        session.add(new_director)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding director: {e}")
    finally:
        session.close()


def get_directors():
    session = get_session()
    try:
        return session.query(Director).all()
    except Exception as e:
        print(f"Error fetching directors: {e}")
        return []
    finally:
        session.close()


def update_director(updated_director: Director):
    session = get_session()
    try:
        director = (session.get(Director, updated_director.director_id))

        if director:
            director.name = updated_director.name
            director.birth_year = updated_director.birth_year
            director.sex = updated_director.sex
            session.commit()
    except Exception as e:
        print(f"Error updating director: {e}")
        return []
    finally:
        session.close()


def delete_director(deleted_director: Director):
    session = get_session()
    try:
        director = session.get(Director, deleted_director.director_id)
        if director:
            session.delete(director)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error deleting director: {e}")
    finally:
        session.close()