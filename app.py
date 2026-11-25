# ============================================================
# WONDERWORLD - MAIN APPLICATION (app.py)
# ============================================================
# This is the main entry point of the WonderWorld website.
# It controls the overall website appearance, logo, navigation
# bar and connection between the different pages.
# ============================================================

##### IMPORT FUNCTIONS ###
import streamlit as st

# Configure general appearance of the website
st.set_page_config(
    page_title="WonderWorld",
    page_icon="🎡",
    layout="wide"
)

# Global CSS styling
st.markdown("""
<style>
    /* Header background */
    [data-testid="stHeader"] {
        background-color: #91C3C2;
    }

    /* Nav links */
    [data-testid="stHeader"] a {
        color: #F4F4F4 !important;
    }

    /* Nav link hover */
    [data-testid="stHeader"] a:hover {
        color: #F4F4F4 !important;
    }

    /* Nav link colour */
    [data-testid="stHeader"] button {
        color: #F4F4F4 !important;
    }

    /* Prevent overflowing content */
    [data-testid="stMain"] {
        overflow-x: clip;
    }

    /* Spacing of container */
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }
</style>
""", unsafe_allow_html=True) # allows Streamlit to interpret the HTML and CSS instead of displaying them as ordinary text.

# website logo
st.logo(
    "https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/1f3a1.svg",
    size="large"
)

# home page nav link
home = st.Page(
    "pages/home.py",
    title="Home",
    default=True # default landing page
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

# combine all pages into 1 navigation menu
pg = st.navigation(
    [home, attractions, planner, tickets],
    position="top"
)

# run the page and any nav links on click
pg.run()