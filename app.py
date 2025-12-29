import streamlit as st
import youtube_downloader

st.set_page_config(layout="wide")
pages = [
    st.Page("pages/search.py", title="Search for Video", icon='🔍'),
    st.Page("pages/randomVideo.py", title="Random Video", icon='🎥'),
]
pages = st.navigation(pages, position="top") # Position the navbar at the top
pages.run()