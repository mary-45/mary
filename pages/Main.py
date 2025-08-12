import streamlit as st
st.set_page_config(
    page_title="CIDATA Dashboard",
    page_icon=":welcome to our dashboard:",
    layout="wide"
)
import pandas as pd
# --- Authentification ---
def check_password():
    def login_form():
        with st.form("login"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Login", on_click=login)

    def login():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "1234":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password.")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_form()
        st.stop()

check_password()
st.title("Welcome to the Home Page")

def home():
    st.title("Welcome to the Home Page")
    st.write("This is the home page of the CIDATA Dashboard. Use the sidebar to navigate through different sections.")
st.sidebar.image("logo.jpeg.jpg", width=150)
st.sidebar.title("Navigation")
df = pd.read_csv(
    "Copie de PAIEMENT_WAVE(1).csv",
    sep=",",                # le séparateur semble être une virgule
    encoding="utf-8-sig",   # pour éviter les caractères invisibles
    dtype=str
)
st.dataframe(df)
import streamlit as st

if st.sidebar.button("🏠 Homepage"):
    st.switch_page("app.py")  # 

if st.sidebar.button("📊 Statistics"):
    st.switch_page("app.py")
