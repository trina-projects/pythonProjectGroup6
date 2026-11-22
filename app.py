import streamlit as st

st.set_page_config(
    page_title="WonderWorld",
    page_icon="🎡",
    layout="wide"
)

st.markdown("""
<style>

    /* Header background */
    [data-testid="stHeader"] {
        background-color: #91C3C2;
    }

    /* Navigation links */
    [data-testid="stHeader"] a {
        color: #F4F4F4 !important;
    }

    /* Navigation link hover */
    [data-testid="stHeader"] a:hover {
        color: #F4F4F4 !important;
    }

    /* Header buttons */
    [data-testid="stHeader"] button {
        color: #F4F4F4 !important;
    }
    

    [data-testid="stMain"] {
        overflow-x: clip;
    }

    /* Normal spacing below the navbar */
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }
</style>
""", unsafe_allow_html=True)



st.logo(
    "assets/main/logo.jpg",
    size="large"
)

home = st.Page(
    "pages/home.py",
    title="Home",
    default=True
)

attractions = st.Page(
    "pages/1_Attractions.py",
    title="Attractions"
)

planner = st.Page(
    "pages/2_Park_Planner.py",
    title="Plan My Visit"
)

tickets = st.Page(
    "pages/3_Tickets.py",
    title="Buy A Ticket"
)

pg = st.navigation(
    [home, attractions, planner, tickets],
    position="top"
)

pg.run()