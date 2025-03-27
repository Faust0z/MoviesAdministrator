from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.associations import movies_have_actors
from models.base import Base


class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    sex = Column(String(20), nullable=False)

    movies = relationship("Movie", secondary=movies_have_actors, back_populates="actors")

    def __init__(self, name, birth_year, sex):
        self.name = name
        self.birth_year = birth_year
        self.sex = sex

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"(name={repr(self.name)},"
                f" birth_year={repr(self.birth_year)},"
                f" sex={repr(self.sex)})"
                )
