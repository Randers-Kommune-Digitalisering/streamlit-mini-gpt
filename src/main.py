import streamlit as st
from streamlit_option_menu import option_menu
from utils.logo import get_logo
from utils.config import ASSISTANT_NAME
from page.assistant import display_assistant_chat
from page.upload_files import upload_files


st.set_page_config(page_title=ASSISTANT_NAME, page_icon="assets/favicon.ico")

with st.sidebar:
    st.sidebar.markdown(get_logo(), unsafe_allow_html=True)
    selected = option_menu(
        str(ASSISTANT_NAME).capitalize(),
        ["Chat", "Håndter dokumenter"],
        default_index=0,
        icons=['activity', 'bi bi-file-earmark-arrow-up'],
        menu_icon="bi bi-robot",
        styles={
            "container": {"padding": "5px", "background-color": "#f0f0f0"},
            "icon": {"color": "#4a4a4a", "font-size": "18px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#d0d0d0", "color": "#4a4a4a"},
            "menu-title": {"font-size": "20px", "font-weight": "bold", "color": "#4a4a4a", "margin-bottom": "10px"},
        }
    )

if selected == "Chat":
    display_assistant_chat()
elif selected == "Håndter dokumenter":
    upload_files()
