import streamlit as st
from streamlit import dialog

from models import Movie
from controllers.movie_controller import get_movies, add_movie, delete_movie, update_movie
from controllers.actor_controller import get_actors
from controllers.genre_controller import get_genres
from controllers.director_controller import get_directors


@dialog("Add a movie")
def dialog_add_movie():
    title = st.text_input("Title")
    release_year = st.number_input("Year", value=2000, min_value=1900, max_value=2100, step=1)
    runtime = st.number_input("Runtime", min_value=1, step=1)

    director_options = {director.name: director.director_id for director in get_directors()}
    selected_director = st.selectbox("Director", options=list(director_options.keys()))

    actor_options = {actor.name: actor for actor in get_actors()}
    selected_actors = st.multiselect("Actors", options=list(actor_options.keys()))

    genres_options = {genre.name: genre for genre in get_genres()}
    selected_genres = st.multiselect("Genres", options=list(genres_options.keys()))

    if st.button("Add Movie"):
        if not title and selected_director and release_year and runtime:
            st.warning("Please fill in all required fields!")

        new_movie = Movie(
            title=title,
            release_year=release_year,
            runtime=runtime,
            director_id=director_options[selected_director]
        )
        new_movie.actors = [actor_options[actor] for actor in selected_actors]
        new_movie.genres = [genres_options[genre] for genre in selected_genres]

        add_movie(new_movie)

        st.success(f"🎬 '{title}' added successfully!")
        st.rerun()


@dialog("Modify a movie")
def dialog_modify_movie():
    movies_options = {movie.title: movie for movie in get_movies()}
    curr_title = st.selectbox("Title", options=list(movies_options.keys()))
    curr_movie: Movie = movies_options[curr_title]

    curr_release_year = curr_movie.release_year
    release_year = st.number_input("Year", value=curr_release_year, min_value=1900, max_value=2100, step=1)
    runtime = st.number_input("Runtime", min_value=1, step=1)

    director_options = {director.name: director.director_id for director in get_directors()}
    curr_director = list(director_options.keys()).index(curr_movie.director.name)
    selected_director = st.selectbox("Director", index=curr_director, options=list(director_options.keys()))

    actor_options = {actor.name: actor for actor in get_actors()}
    curr_actors = [actor.name for actor in curr_movie.actors]
    selected_actors = st.multiselect("Actors", default=curr_actors, options=list(actor_options.keys()))

    genres_options = {genre.name: genre for genre in get_genres()}
    curr_genres = {genre.name for genre in curr_movie.genres}
    selected_genres = st.multiselect("Genres", default=curr_genres, options=list(genres_options.keys()))

    if st.button("Update Selected Movie"):
        if not curr_title and selected_director and release_year and runtime:
            st.warning("Please fill in all required fields!")

        curr_movie.release_year = release_year
        curr_movie.runtime = runtime
        curr_movie.director_id = director_options[selected_director]
        curr_movie.actors = [actor_options[actor] for actor in selected_actors]
        curr_movie.genres = [genres_options[genre] for genre in selected_genres]

        update_movie(curr_movie)

        st.success(f"🎬 '{curr_title}' updated successfully!")
        st.rerun()

    if st.button("Delete Selected Movie"):
        delete_movie(curr_movie)
        st.success(f"🎬 '{curr_title}' deleted successfully!")
        st.rerun()
