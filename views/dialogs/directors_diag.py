import streamlit as st
from streamlit import dialog

from controllers.director_controller import add_director, get_directors, update_director, delete_director
from models.base import get_session
from models.director import Director


@dialog("Add a Director")
def dialog_add_director():
    name = st.text_input("Name")
    birth_year = st.number_input("Birth Year", value=2000, min_value=1900, step=1)
    sex = st.selectbox("Sex", options=["Male", "Female", "Other"])

    if st.button("Add Director"):
        if not name and birth_year and sex:
            st.warning("Please fill in all required fields!")
        else:
            new_director = Director(
                name=name,
                birth_year=birth_year,
                sex=sex
            )

            add_director(new_director, get_session())
            st.success(f"🎬 '{new_director.director_id}: {name}' added successfully!")
            # st.rerun()


@dialog("Modify an Director")
def dialog_modify_director():
    directors_values_map = {f"{director.director_id}: {director.name}": director for director in get_directors()}
    curr_director: Director = directors_values_map[st.selectbox("Select a Director", options=list(directors_values_map.keys()))]

    name = st.text_input("Name", value=curr_director.name)
    birth_year = st.number_input("Year", value=curr_director.birth_year, min_value=1900, step=1)
    sex_list = ["Male", "Female", "Other"]
    sex = st.selectbox("Sex", index=sex_list.index(curr_director.sex), options=sex_list)

    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("Update Selected Director"):
            if not sex and birth_year:
                st.warning("Please fill in all required fields!")
            else:
                curr_director.name = name
                curr_director.birth_year = birth_year
                curr_director.sex = sex

                update_director(curr_director)
                # st.success(f"🎬 '{curr_director.director_id}: {name}' updated successfully!")
                st.rerun()

    with col2:
        if st.button("Delete Selected Director"):
            if any(curr_director.movies):
                st.warning(f"⚠ Can't delete '{curr_director.director_id}: {name}' because there are movies directed by them.")
            else:
                delete_director(curr_director)
                # st.success(f"🎬 '{curr_director.director_id}: {name}' deleted successfully!")
                st.rerun()
