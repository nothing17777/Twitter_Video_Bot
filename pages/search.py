import streamlit as st
from downloader import youtube_downloader
import format.format as format

if 'query' not in st.session_state:
    st.session_state.query = None
if 'videos' not in st.session_state:
    st.session_state.videos = None
if 'search' not in st.session_state:
    st.session_state.search = None
if 'results_visible' not in st.session_state:
    st.session_state.results_visible = False

st.title("Search Youtube Video")

with st.container(border=True):
    col1, col2 = st.columns([0.8,0.2], vertical_alignment='bottom')
    with col1:
        st.session_state.query = st.text_input("Video Keywords")
    with col2:
        st.session_state.search = st.button("Search", width='stretch')

if st.session_state.search:
    st.session_state.videos = youtube_downloader.searchVideosUnderTwoMin(st.session_state.query, limit=2)
    st.session_state.results_visible = True

if st.session_state.results_visible and st.session_state.videos:
    for video in st.session_state.videos:
        with st.container(border=True):
            col1, col2 = st.columns([0.8,0.2], vertical_alignment='center')
            url = video['url']
            with col1:
                st.image(video['thumbnails'][0]['url'], width = 'stretch')
            with col2:
                st.write(f"Description: {video['description']}")
                st.write(f"Duration: {video['duration'] } seconds")
                st.write(f"Author: {video['uploader']}")
                st.write(f"Views: {video['view_count']}")
                with st.spinner("Loading Comments..."):
                    comments = youtube_downloader.get_top_comments(url)
                for comment in comments:
                    st.write(comment)
                if st.button("Add to Used", key=url):
                    with st.spinner("Adding to used list..."):
                        youtube_downloader.add_used_video(url)
                    st.success("Video added to used list")


