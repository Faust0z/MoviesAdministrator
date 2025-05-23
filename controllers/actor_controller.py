from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, Session

from models.actor import Actor
from models.base import get_session
from models.movie import Movie


def add_actor(new_actor: Actor, session: Session):
    try:
        with session.begin():
            session.add(new_actor)

    except Exception as e:
        print(f"Error fetching actors/actresses: {e}")
        return []


def get_actors(session: Session = None):
    session = session or get_session()
    try:
        stmt = select(Actor).options(joinedload(Actor.movies))
        return session.scalars(stmt).unique().all()

    except Exception as e:
        print(f"Error fetching actors: {e}")
        return []


def get_actors_dict(filter_value: str = None, session: Session = None):
    session = session or get_session()
    try:
        like_pattern = f"%{filter_value}%"
        filters = [
            field.ilike(like_pattern)
            for field in [Movie.title, Actor.name, Actor.sex, Actor.birth_year]
        ] if filter_value else []

        stmt = (
            select(Actor).distinct()
            .outerjoin(Actor.movies)
            .options(joinedload(Actor.movies))
        )

        if filters:
            stmt = stmt.where(or_(*filters))

        with session.begin():
            actors = session.execute(stmt).unique().scalars().all()
            return [actor.to_dict() for actor in actors]

    except Exception as e:
        print(f"Error fetching actors: {e}")
        return []


def update_actor(updated_actor: Actor):
    session = get_session()
    try:
        with session.begin():
            actor = session.get(Actor, updated_actor.actor_id)

            if actor:
                actor.name = updated_actor.name
                actor.birth_year = updated_actor.birth_year
                actor.sex = updated_actor.sex

    except Exception as e:
        print(f"Error updating actor: {e}")
        return []


def delete_actor(deleted_actor: Actor):
    session = get_session()
    try:
        with session.begin():
            actor = session.get(Actor, deleted_actor.actor_id)
            if actor:
                session.delete(actor)

    except Exception as e:
        print(f"Error deleting actor: {e}")
