import basic
import goals
import eda_districs
import eda_schools
import streamlit as st

PAGES = {
    "Goals": goals,
    "Basic Analytics": basic,
    "School Districs EDA": eda_districs,
    "Further EDA at School level": eda_schools
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()