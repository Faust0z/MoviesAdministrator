from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Director(Base):
    __tablename__ = "directors"

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    sex = Column(String(100), nullable=False)

    movies = relationship("Movie", back_populates="director")

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
