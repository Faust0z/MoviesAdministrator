import streamlit as st
import pandas as pd

from views.dialogs.movies_diag import dialog_add_movie, dialog_modify_movie
from controllers.movie_controller import get_movies
from controllers.actor_controller import get_actors
from controllers.genre_controller import get_genres
from controllers.director_controller import get_directors


def main():
    st.title("Movies Admin")

    movies_tab, actors_tab, directors_tab, genres_tab = st.tabs(["Movies", "Actors", "Directors", "Genres"])
    with movies_tab:
        display_movie_list()
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a movie"):
                dialog_add_movie()
        with col2:
            if st.button("Modify a movie"):
                dialog_modify_movie()

    with actors_tab:
        display_actors_list()
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add an actor"):
                dialog_add_movie()
        with col2:
            if st.button("Modify an actor"):
                dialog_modify_movie()

    with directors_tab:
        display_directors_list()
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a director"):
                pass
        with col2:
            if st.button("Modify a director"):
                pass

    with genres_tab:
        display_genres_list()
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a genre"):
                pass
        with col2:
            if st.button("Modify a genre"):
                pass


def display_movie_list():
    movies_data = [
        {"ID": movie.movie_id,
         "Title": movie.title,
         "Release Year": movie.release_year,
         "Runtime": movie.runtime,
         "Director name": movie.director.name,
         "Actors": ", ".join(actor.name for actor in movie.actors),
         "Genres": ", ".join(genre.name for genre in movie.genres)
         } for movie in get_movies()
    ]
    df = pd.DataFrame(movies_data)
    st.dataframe(df)


def display_actors_list():
    actors_data = [
        {"ID": actor.actor_id,
         "Name": actor.name,
         "Birth Year": actor.birth_year,
         "Sex": actor.sex,
         "Movies": ", ".join(movie.title for movie in actor.movies)
         } for actor in get_actors()
    ]
    df = pd.DataFrame(actors_data)
    st.dataframe(df)


def display_directors_list():
    directors_data = [
        {"ID": direct.director_id,
         "Name": direct.name,
         "Birth Year": direct.birth_year,
         "Sex": direct.sex,
         "Movies": ", ".join(movie.title for movie in direct.movies)  # Todo: this doesn't works this way
         } for direct in get_directors()
    ]
    df = pd.DataFrame(directors_data)
    st.dataframe(df)


def display_genres_list():
    pass
