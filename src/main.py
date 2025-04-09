import streamlit as st
from streamlit_option_menu import option_menu
from utils.logo import get_logo
from page.assistant import display_hjælpemiddel_chat


st.set_page_config(page_title="Hjælpemiddelområdets Mini GPT", page_icon="assets/favicon.ico")

with st.sidebar:
    st.sidebar.markdown(get_logo(), unsafe_allow_html=True)
    selected = option_menu(
        "Hjælpemiddelområdets Mini GPT",
        ["Hjælpemiddelområdets Assistant Chat"],
        default_index=0,
        icons=['list-task', 'activity', 'cloud-upload'],
        menu_icon="cast",
        styles={
            "container": {"padding": "5px", "background-color": "#f0f0f0"},
            "icon": {"color": "#4a4a4a", "font-size": "18px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#d0d0d0", "color": "#4a4a4a"},
            "menu-title": {"font-size": "20px", "font-weight": "bold", "color": "#4a4a4a", "margin-bottom": "10px"},
        }
    )

if selected == "Hjælpemiddelområdets Assistant Chat":
    display_hjælpemiddel_chat()
