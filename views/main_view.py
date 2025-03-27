import streamlit as st
import pandas as pd
from streamlit import dialog

from controllers.movie_controller import get_movies, add_movie, delete_movie, update_movie
from controllers.director_controller import get_directors
from controllers.actor_controller import get_actors
from controllers.genre_controller import get_genres
from models import Movie


def main():
    st.title("Movies Admin")
    display_movie_list()
    if st.button("Add movie"):
        display_add_movie()
    # display_actors_list()
    # display_add_actor()

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
    st.table(df)

@dialog("Add a movie")
def display_add_movie():
    # st.subheader("Add a movie")
    title = st.text_input("Title", key="movie_title")
    release_year = st.number_input("Year", value=2000, min_value=1900, max_value=2100, step=1, key="movie_year")
    runtime = st.number_input("Runtime", min_value=1, step=1, key="movie_runtime")

    director_options = {director.name: director.director_id for director in get_directors()}
    selected_director = st.selectbox("Director", options=list(director_options.keys()), key="movie_director")

    actor_options = {actor.name: actor for actor in get_actors()}
    selected_actors = st.multiselect("Actors", options=list(actor_options.keys()), key="movie_actors")

    # Hacer lo mismo para genres
    if st.button("Add Movie"):
        if title and selected_director:
            new_movie = Movie(
                title=title,
                release_year=release_year,
                runtime=runtime,
                director_id=director_options[selected_director]
            )
            new_movie.actors = [actor_options[actor] for actor in selected_actors]

            add_movie(new_movie)

            st.success(f"🎬 '{title}' added successfully!")
            st.rerun()
        else:
            st.warning("Please fill in all required fields!")