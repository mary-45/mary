import plotly.express as px
from PIL import Image
st.set_page_config(
    st.title

)

def home():
    st.title("Welcome to the Home Page")
    st.write("This is the home page of the CIDATA Dashboard. Use the sidebar to navigate through different sections.")

def check_password():
    def login_form():
        with st.form("login"):
            st.text_input("Username", key="username")
            st.text_input("password", type="password", key="password")
            st.form_submit_button("login", on_click=login)

    def login():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "1234":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password try again.")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_form()
        st.stop()

check_password()
st.success("succesful login ! You can now go to the Home page.")

# reading the data from the excel csv file
df = pd.read_csv('copie de PAIEMENT_WAVE(1).csv', sep=',')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = image.open('logo.jpeg.jpg')
col1, col2 = st.columns([1, 2])
with col1:
    st.image(image, width=200)
with col2:
    st.title("Dashboard CIDATA - Payment by Wave")
   

# Display the dataframe in the Streamlit app

st.write("This is a simple dashboard to visualize payment data.")
# Your Streamlit app code goes here
import streamlit as st
import pandas as pd
# Lecture du CSV
df = pd.read_csv("Copie de PAIEMENT_WAVE(1).csv", sep=",")

# Affiche les colonnes pour vérifier
st.write("Columns of the DataFrame :", df.columns.tolist())
st.subheader("📊 Data payment")
st.dataframe(df)


# Nettoyage et conversion de la colonne 'prices'
def clean_price(x):
    if pd.isna(x):
        return 0
    x = str(x).replace("XOF", "").replace("FCFA", "").replace(",", "").replace(" ", "")
    try:
        return float(x)
    except:
        return 0

df["prices"] = df["prices"].apply(clean_price)

# Statistiques
st.metric("💰 Total payment", f"{df['prices'].sum():,.0f} FCFA")
st.metric("📦 Total User Transactions", len(df))

# Chart: Nombre de transactions par ville
if "city" in df.columns:
    st.subheader("Total payments per city (progress view)")
    payments_per_city = df.groupby("city")["prices"].sum().reset_index()

    st.data_editor(
        payments_per_city,
        column_config={
            "prices": st.column_config.ProgressColumn(
                "Total Payment",
                help="Total payment in FCFA",
                format="%.0f FCFA",
                min_value=0,
                max_value=float(payments_per_city["prices"].max()),
            ),
        },
        hide_index=True,
    )

    # Filtre par ville
    ville = st.selectbox("Choose a city :", sorted(df["city"].dropna().unique()))
    df_city = df[df["city"] == ville]

    st.subheader(f"Types de montants pour {ville}")
    prix_types = df_city.groupby("prices").size().reset_index(name="Total user transactions")
    st.dataframe(prix_types)


    # Chart: Nombre de transactions par type de montant pour la ville sélectionnée
    fig_types = px.pie(prix_types, names="prices", values="Total user transactions", title=f"Répartition des montants pour {ville}")
    st.plotly_chart(fig_types)

    st.metric("💰 Total payment for this city", f"{df_city['prices'].sum():,.0f} FCFA")
    st.metric("📦 Total user transactions", len(df_city))

