import pandas as pd
import streamlit as st

from controllers.actor_controller import get_actors_dict
from controllers.director_controller import get_directors_dict
from controllers.genre_controller import get_genres_dict
from controllers.movie_controller import get_movies_dict
from views.dialogs.actors_diag import dialog_add_actor, dialog_modify_actor
from views.dialogs.directors_diag import dialog_add_director, dialog_modify_director
from views.dialogs.genres_diag import dialog_add_genre, dialog_delete_genre
from views.dialogs.movies_diag import dialog_add_movie, dialog_modify_movie


def main():
    st.title("Movies Admin")

    movies_tab, actors_tab, directors_tab, genres_tab = st.tabs(["Movies", "Actors", "Directors", "Genres"])
    with movies_tab:
        display_movie_list(filter_value=st.text_input("Search a Movie"))
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a movie"):
                dialog_add_movie()
        with col2:
            if st.button("Modify a movie"):
                dialog_modify_movie()
        st.write("Warning: there must be directors loaded to add movies")

    with actors_tab:
        display_actors_list(filter_value=st.text_input("Search an Actor/Actresses"))
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add an actor"):
                dialog_add_actor()
        with col2:
            if st.button("Modify an actor"):
                dialog_modify_actor()

    with directors_tab:
        display_directors_list(filter_value=st.text_input("Search a Director"))
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a director"):
                dialog_add_director()
        with col2:
            if st.button("Modify a director"):
                dialog_modify_director()

    with genres_tab:
        display_genres_list(filter_value=st.text_input("Search a Genre"))
        spacer1, col1, col2, spacer2 = st.columns([3, 2, 2, 3])
        with col1:
            if st.button("Add a genre"):
                dialog_add_genre()
        with col2:
            if st.button("Modify a genre"):
                dialog_delete_genre()


def display_movie_list(filter_value: str):
    movies_data = get_movies_dict(filter_value)
    if movies_data:
        df = pd.DataFrame(movies_data)
        st.dataframe(df)
    else:
        st.write("No movies found")


def display_actors_list(filter_value: str):
    actors_data = get_actors_dict(filter_value)
    if actors_data:
        df = pd.DataFrame(actors_data)
        st.dataframe(df)
    else:
        st.write("No actors/actresses found")


def display_directors_list(filter_value: str):
    directors_data = get_directors_dict(filter_value)
    if directors_data:
        df = pd.DataFrame(directors_data)
        st.dataframe(df)
    else:
        st.write("No directors found")


def display_genres_list(filter_value: str):
    genres_data = get_genres_dict(filter_value)
    if genres_data:
        df = pd.DataFrame(genres_data)
        st.dataframe(df)
    else:
        st.write("No genres found")
