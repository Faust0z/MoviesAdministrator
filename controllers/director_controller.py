from models.base import get_session
from models.director import Director

def get_directors():
    session = get_session()
    try:
        return session.query(Director).all()
    except Exception as e:
        print(f"Error fetching directors: {e}")
        return []
    finally:
        session.close()

