import streamlit as st

st.set_page_config(
    page_title="Theme Park Planner",
    page_icon="🎢",
    layout="wide"
)

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True
)

attractions = st.Page(
    "pages/1_Attractions.py",
    title="Attractions",
    icon="🎢"
)

planner = st.Page(
    "pages/2_Park_Planner.py",
    title="Park Planner",
    icon="🗺️"
)

pg = st.navigation(
    [home, attractions, planner],
    position="top"
)

pg.run()