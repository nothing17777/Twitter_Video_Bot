import streamlit as st
import youtube_downloader

st.title("Search Youtube Video")

with st.container(border=True):
    col1, col2 = st.columns([0.8,0.2], vertical_alignment='bottom')
    with col1:
        Query = st.text_input("Video Keywords")
    with col2:
        search = st.button("Search", width='stretch')

if search:
    videos = youtube_downloader.searchVideosUnderTwoMin(Query)
    for video in videos:
        with st.container(border=True):
            col1, col2 = st.columns([0.8,0.2], vertical_alignment='bottom')
            url = video['url']
            with col1:
                st.image(video['thumbnails'][0]['url'])
                st.video(video['url'])
            with col2:
                st.write(f"Duration: {video['duration'] } seconds")
                st.write(f"Author: {video['uploader']}")
                st.write(f"Views: {video['view_count']}")
                with st.spinner("Loading Comments..."):
                    comments = youtube_downloader.get_top_comments(url)
                for comment in comments:
                    st.write(comment)


