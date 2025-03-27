from models.base import get_session
from models.genre import Genre

def get_genres():
    session = get_session()
    try:
        return session.query(Genre).all()
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return []
    finally:
        session.close()

