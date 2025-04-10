import streamlit as st
from streamlit import dialog

from controllers.genre_controller import add_genre, get_genres, update_genre, delete_genre
from models.base import get_session
from models.genre import Genre


@dialog("Add a genre")
def dialog_add_genre():
    name = st.text_input("Name")

    if st.button("Add Genre"):
        if not name:
            st.warning("Please fill in all required fields!")
        else:
            add_genre(Genre(name=name), get_session())
            st.success(f"🎬 '{name}' added successfully!")
            # st.rerun()


@dialog("Modify a Genre")
def dialog_delete_genre():
    genres_values_map = {f"{genre.genre_id}: {genre.name}": genre for genre in get_genres()}
    curr_genre: Genre = genres_values_map[st.selectbox("Select a genre", options=list(genres_values_map.keys()))]

    name = st.text_input("Name", value=curr_genre.name)

    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("Update Selected Genre"):
            if not name:
                st.warning("Please fill in all required fields!")
            else:
                curr_genre.name = name

                update_genre(curr_genre)
                # st.success(f"🎬 '{curr_genre.genre_id}: {name}' updated successfully!")
                st.rerun()

    with col2:
        if st.button("Delete Selected Genre"):
            delete_genre(curr_genre)
            # st.success(f"🎬 '{curr_genre.genre_id}: {name}' deleted successfully!")
            st.rerun()
