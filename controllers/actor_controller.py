from models.base import get_session
from models.actor import Actor

def get_actors():
    session = get_session()
    try:
        return session.query(Actor).all()
    except Exception as e:
        print(f"Error fetching actor: {e}")
        return []
    finally:
        session.close()

