import streamlit as st
from streamlit import dialog

from controllers.actor_controller import add_actor, get_actors, update_actor, delete_actor
from models.actor import Actor
from models.base import get_session


@dialog("Add an actor")
def dialog_add_actor():
    name = st.text_input("Name")
    birth_year = st.number_input("Birth Year", value=2000, min_value=1900, step=1)
    sex = st.selectbox("Sex", options=["Male", "Female", "Other"])

    if st.button("Add Actor"):
        if not name and birth_year and sex:
            st.warning("Please fill in all required fields!")
        else:
            new_actor = Actor(
                name=name,
                birth_year=birth_year,
                sex=sex,
            )

            add_actor(new_actor, get_session())
            st.success(f"🎬 '{name}' added successfully!")
            # st.rerun()


@dialog("Modify an Actor/Actress")
def dialog_modify_actor():
    actors_values_map = {f"{actor.actor_id}: {actor.name}": actor for actor in get_actors()}
    curr_actor: Actor = actors_values_map[st.selectbox("Select an actor/actress", options=list(actors_values_map.keys()))]

    name = st.text_input("Name", value=curr_actor.name)
    birth_year = st.number_input("Year", value=curr_actor.birth_year, min_value=1900, step=1)
    sex_list = ["Male", "Female", "Other"]
    sex = st.selectbox("Sex", index=sex_list.index(curr_actor.sex), options=sex_list)

    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("Update Selected Actor"):
            if not name and sex and birth_year:
                st.warning("Please fill in all required fields!")
            else:
                curr_actor.name = name
                curr_actor.birth_year = birth_year
                curr_actor.sex = sex

                update_actor(curr_actor)
                # st.success(f"🎬 '{curr_actor.actor_id}: {name}' updated successfully!")
                st.rerun()

    with col2:
        if st.button("Delete Selected Actor"):
            delete_actor(curr_actor)
            # st.success(f"🎬 '{curr_actor.actor_id}: {name}' deleted successfully!")
            st.rerun()
