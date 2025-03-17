from models.models import engine, Director, Actor, Genre, Movie
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    session.commit()