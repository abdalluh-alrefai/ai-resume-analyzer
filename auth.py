import streamlit as st
from database import create_user, get_user


def login_page():

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = get_user(username, password)

        if user:
            st.session_state["user"] = user
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")


def signup_page():

    st.title("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):

        success = create_user(username, password)

        if success:
            st.success("Account created. You can login now.")
        else:
            st.error("Username already exists")