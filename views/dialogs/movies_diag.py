import streamlit as st
from streamlit import dialog

from controllers.actor_controller import get_actors
from controllers.director_controller import get_directors
from controllers.genre_controller import get_genres
from controllers.movie_controller import add_movie, update_movie, delete_movie, get_movies
from models.base import get_session
from models.movie import Movie


@dialog("Add a movie")
def dialog_add_movie():
    # I create the session here to prevent problems of manipulating the same data from different sessions when adding the movie
    session = get_session()
    director_options = {direc.name: direc for direc in get_directors(session)}
    actor_options = {actor.name: actor for actor in get_actors(session)}
    genres_options = {genre.name: genre for genre in get_genres(session)}
    # Need to reset the session afterward or the add_movie method won't work
    session.reset()

    title = st.text_input("Title")
    release_year = st.number_input("Year", value=2000, min_value=1900, max_value=2100, step=1)
    runtime = st.number_input("Runtime", min_value=1, step=1)
    selected_director = st.selectbox("Director", options=list(director_options.keys()))
    selected_actors = st.multiselect("Actors", options=list(actor_options.keys()))
    selected_genres = st.multiselect("Genres", options=list(genres_options.keys()))

    if st.button("Add Movie"):
        if not title and selected_director and release_year and runtime:
            st.warning("Please fill in all required fields!")
        else:
            new_movie = Movie(
                title=title,
                release_year=release_year,
                runtime=runtime,
                director_id=director_options[selected_director].director_id
            )
            new_movie.actors = [actor_options[actor] for actor in selected_actors]
            new_movie.genres = [genres_options[genre] for genre in selected_genres]

            add_movie(new_movie, session)
            st.success(f"🎬 '{new_movie.movie_id}: {title}' added successfully!")
            # st.rerun()


@dialog("Modify a movie")
def dialog_modify_movie():
    session = get_session()
    with session.begin():
        movies_values_map = {(f"{movie.movie_id}: "
                              f"{movie.title} - "
                              f"{movie.release_year} - "
                              f"{movie.director.name}"): movie for movie in get_movies(session)}
        curr_movie: Movie = movies_values_map[st.selectbox("Select a movie", options=list(movies_values_map.keys()))]
        director_options = {direc.name: direc for direc in get_directors(session)}
        actor_options = {actor.name: actor for actor in get_actors(session)}
        genres_options = {genre.name: genre for genre in get_genres(session)}

        curr_director = list(director_options.keys()).index(curr_movie.director.name)
        curr_actors = [actor.name for actor in curr_movie.actors]
        curr_genres = {genre.name for genre in curr_movie.genres}

    title = st.text_input("Title", value=curr_movie.title)
    release_year = st.number_input("Year", value=curr_movie.release_year, min_value=1900, max_value=2100, step=1)
    runtime = st.number_input("Runtime", value=curr_movie.runtime, min_value=1, step=1)
    selected_director = st.selectbox("Director", index=curr_director, options=list(director_options.keys()))
    selected_actors = st.multiselect("Actors", default=curr_actors, options=list(actor_options.keys()))
    selected_genres = st.multiselect("Genres", default=curr_genres, options=list(genres_options.keys()))

    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("Update Selected Movie"):
            if not curr_movie and selected_director and release_year and runtime:
                st.warning("Please fill in all required fields!")
            else:
                curr_movie.title = title
                curr_movie.release_year = release_year
                curr_movie.runtime = runtime
                curr_movie.director_id = director_options[selected_director].director_id
                curr_movie.actors = [actor_options[actor] for actor in selected_actors]
                curr_movie.genres = [genres_options[genre] for genre in selected_genres]

                update_movie(curr_movie)
                # st.success(f"🎬 '{curr_movie.movie_id}: {title}' updated successfully!")
                st.rerun()

    with col2:
        if st.button("Delete Selected Movie"):
            delete_movie(curr_movie)
            # st.success(f"🎬 '{curr_movie.movie_id}: {title}' deleted successfully!")
            st.rerun()
