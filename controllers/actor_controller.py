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
    session = session if session else get_session()
    try:
        return (session.query(Actor)
                .options(joinedload(Actor.movies))
                .all())
    except Exception as e:
        print(f"Error fetching actors: {e}")
        return []


def get_actors_dict(filter_value: str = None, session: Session = None):
    session = session if session else get_session()
    try:
        filters = []
        if filter_value:
            like_pattern = f"%{filter_value}%"
            filters.append(Movie.title.ilike(like_pattern))
            filters.append(Actor.name.ilike(like_pattern))
            filters.append(Actor.sex.ilike(like_pattern))
            filters.append(Actor.birth_year.ilike(like_pattern))

        stmt = (
            select(Actor).distinct()
            .outerjoin(Actor.movies)
            .options(joinedload(Actor.movies))
        )

        if filters:
            stmt = stmt.where(or_(*filters))

        with session.begin():
            actors = session.execute(stmt).unique().scalars().all()
            return [{
                "ID": actor.actor_id,
                "Name": actor.name,
                "Birth Year": actor.birth_year,
                "Sex": actor.sex,
                "Movies": ", ".join(movie.title for movie in actor.movies)
            } for actor in actors
            ]
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
