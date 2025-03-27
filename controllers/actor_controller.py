from sqlalchemy.orm import joinedload

from models.base import get_session
from models.actor import Actor


def add_actor(new_actor: Actor):
    session = get_session()
    try:
        session.add(new_actor)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding actor: {e}")
    finally:
        session.close()


def get_actors():
    session = get_session()
    try:
        return (session.query(Actor)
                .options(joinedload(Actor.movies))
                .all())
    except Exception as e:
        print(f"Error fetching actors: {e}")
        return []
    finally:
        session.close()


def update_actor(updated_actor: Actor):
    session = get_session()
    try:
        actor = (session.get(Actor, updated_actor.actor_id)
                 .options(joinedload(Actor.movies)))

        if actor:
            actor.name = updated_actor.name
            actor.birth_year = updated_actor.birth_year
            actor.sex = updated_actor.sex
            actor.movies = [session.merge(movie) for movie in updated_actor.movies]
            session.commit()
    except Exception as e:
        print(f"Error updating actor: {e}")
        return []
    finally:
        session.close()


def delete_actor(deleted_actor: Actor):
    session = get_session()
    try:
        actor = session.get(Actor, deleted_actor.actor_id)
        if actor:
            session.delete(actor)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error deleting actor: {e}")
    finally:
        session.close()
