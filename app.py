import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.express as px

from streamlit_option_menu import option_menu

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

# --- Sidebar ---
st.sidebar.image("logo.jpeg.jpg", width=100)
st.sidebar.title("CIDATA Dashboard Menu")

with st.sidebar:
    page = option_menu(
        "Menu",
        ["Home", "About", "Contact"],
        icons=["house", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# --- Load data (une seule fois) ---
df = pd.read_csv(
    "Copie de PAIEMENT_WAVE(1).csv",
    sep=",",                # le séparateur semble être une virgule
    encoding="utf-8-sig",   # pour éviter les caractères invisibles
    dtype=str               # garde les données brutes pour nettoyage
)

col1, col2 = st.columns([1, 2])
with col1:
    image = Image.open("logo.jpeg.jpg")
    st.image(image, width=200)
with col2:
    st.title("Dashboard CIDATA - Payment by Wave")
    st.write("This dashboard visualizes Wave payment data.")

# Nettoyage des prix
def clean_price(x):
    if pd.isna(x):
        return 0
    x = str(x).replace("XOF", "").replace("FCFA", "").replace(",", "").replace(" ", "")
    try:
        return float(x)
    except:
        return 0

df["prices"] = df["prices"].apply(clean_price)
df["date of creation"] = pd.to_datetime(df["date of creation"], errors="coerce")

# --- Page: Home ---
if page == "Home":
    # Tableau du total des paiements par mois (avant tout)
    df["month"] = df["date of creation"].dt.to_period("M")
    payments_per_month = df.groupby("month")["prices"].sum().reset_index()
    payments_per_month["month"] = payments_per_month["month"].astype(str)

    st.metric(label="💰 Total money earned", value=f"{df['prices'].sum():,.0f} FCFA")

    # ----------- FILTRE CALENDRIER -----------
    min_date = df["date of creation"].min().date()
    max_date = df["date of creation"].max().date()
    selected_date = st.date_input("Choose date :", min_value=min_date, max_value=max_date, value=min_date)
    filtered_df = df[df["date of creation"].dt.date == selected_date]

    # --- Métriques principales (2 colonnes égales) ---
    col1, col2 = st.columns(2)
    col1.metric("💰 Total Payment", f"{filtered_df['prices'].sum():,.0f} FCFA")
    col2.metric("📦 Total users Transactions", len(filtered_df))

    # --- Aperçu des données ---
    st.subheader("📊 Data Overview")
    st.dataframe(filtered_df.head(200))

    # --- Paiements par ville ---
    if "city" in filtered_df.columns:
        st.subheader("Total Payments per City")
        payments_per_city = filtered_df.groupby("city")["prices"].sum().reset_index()

        st.data_editor(
            payments_per_city,
            column_config={
                "prices": st.column_config.ProgressColumn(
                    "Total Payment (FCFA)",
                    help="Total payment in FCFA",
                    format="%.0f FCFA",
                    min_value=0,
                    max_value=float(payments_per_city["prices"].max()) if not payments_per_city.empty else 1,
                ),
            },
            hide_index=True,
        )

        # Filtrer une ville
        ville = st.selectbox("Choose a city:", sorted(filtered_df["city"].dropna().unique()))
        df_city = filtered_df[filtered_df["city"] == ville]

        st.subheader(f"Payment Types in {ville}")
        prix_types = df_city.groupby("prices").size().reset_index(name="Total Transactions")
        st.dataframe(prix_types)

        if not prix_types.empty:
            fig_types = px.pie(prix_types, names="prices", values="Total Transactions", title=f"Total des paiements à {ville}")
            st.plotly_chart(fig_types)

        # --- Métriques par ville (2 colonnes égales) ---
        col1, col2 = st.columns(2)
        col1.metric("💰 Total payment (city)", f"{df_city['prices'].sum():,.0f} FCFA")
        col2.metric("📦 Transactions (city)", len(df_city))

# --- Page: About ---
elif page == "About":
    st.title("ℹ️ About")
    st.write("This dashboard is created to analyze Wave payments for CIDATA.")
    st.write("- Created by Marie")
    st.write("- Built with Streamlit")

# --- Page: Contact ---
elif page == "Contact":
    st.title("📞 Contact")
    st.write("You can reach us at:")
    st.write("- 📧 Email: contact@cidata.com")
    st.write("- 📞 Phone: +225 07 00 00 00 00")


