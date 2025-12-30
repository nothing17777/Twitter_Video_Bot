import streamlit as st

st.set_page_config(layout="wide")
pages = [
    st.Page("pages/search.py", title="Search for Video", icon='🔍'),
    st.Page("pages/randomVideo.py", title="Random Video", icon='🎥'),
    st.Page("pages/tiktok.py", title="Tiktok Video", icon='🎥'),
]
pages = st.navigation(pages, position="top") # Position the navbar at the top
pages.run()