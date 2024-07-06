import streamlit as st
from create_application import new_application
from admin_login import admin_panel

st.set_page_config(page_title="Subway Application Management", page_icon=":sandwich:", layout="wide")

st.image("subway.png", width=200)
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select a page", ["Create New Application", "Admin Panel"])

if option == "Create New Application":
    new_application()
elif option == "Admin Panel":
    admin_panel()