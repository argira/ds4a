import basic
import goals
import eda_districs
import eda_schools
import eda_ethnicities
import streamlit as st

PAGES = {
    "Goals": goals,
    "Basic Analysis": basic,
    "Extended EDA": eda_districs,
    "Further EDA at School level": eda_schools,
    "Analysis for Ethnicities": eda_ethnicities
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()