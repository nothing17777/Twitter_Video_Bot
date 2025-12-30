import streamlit as st
from downloader import tiktok_downloader
from uploader import youtube_upload as youtube_uploader
import os
import random

st.title("TikTok Video Downloader")

# Initialize session state for tracking downloaded video and form inputs
if 'downloaded_info' not in st.session_state:
    st.session_state.downloaded_info = None
if 'edit_title' not in st.session_state:
    st.session_state.edit_title = ""
if 'edit_description' not in st.session_state:
    st.session_state.edit_description = ""
if 'edit_tags' not in st.session_state:
    st.session_state.edit_tags = "shorts, trending, viral, funnycat, aicat, aistory"

with st.container(border=True):
    url = st.text_input("Enter TikTok URL", placeholder="https://www.tiktok.com/...")
    
    if st.button("Download", use_container_width=True):
        if url:
            with st.status("Downloading video...", expanded=True) as status:
                info = tiktok_downloader.download_tiktok_video(url, output_path='downloads')
                if info:
                    st.session_state.downloaded_info = info
                    # Pre-fill the form with defaults
                    base_title = random.choice(youtube_uploader.titles) if hasattr(youtube_uploader, 'titles') else info.get('title', 'AI Cat Moment')
                    st.session_state.edit_title = base_title
                    st.session_state.edit_description = f"{base_title}\n\n#Shorts #Trending #Viral #Funnycat #AICat #AIStory\nAI-generated cat 🐱\nScroll if you dare."
                    
                    status.update(label="Download Complete!", state="complete", expanded=False)
                    st.success(f"✅ Video downloaded!")
                else:
                    st.session_state.downloaded_info = None
                    status.update(label="Download Failed", state="error", expanded=False)
                    st.error("Failed to download the video. Please check the URL.")
        else:
            st.warning("Please enter a TikTok URL.")

# Only show upload section if a video has been downloaded
if st.session_state.downloaded_info:
    with st.container(border=True):
        st.subheader("YouTube Upload Settings")
        
        # User input fields
        final_title = st.text_input("Video Title", value=st.session_state.edit_title, max_chars=100)
        final_description = st.text_area("Video Description", value=st.session_state.edit_description, height=150)
        final_tags_str = st.text_input("Tags (comma separated)", value=st.session_state.edit_tags)
        
        if st.button("Start Upload", use_container_width=True):
            video_file = 'downloads/catMemeVideo.mp4'
            
            if not os.path.exists(video_file):
                st.error("Video file not found. Please download it again.")
                st.stop()

            with st.spinner("Connecting to YouTube..."):
                try:
                    youtube = youtube_uploader.get_authenticated_service()
                except Exception as e:
                    st.error(f"Failed to connect to YouTube: {e}")
                    st.stop()

            with st.spinner("Uploading to YouTube..."):
                try:
                    # Convert tags string back to list
                    tags_list = [t.strip() for t in final_tags_str.split(",") if t.strip()]
                    
                    result = youtube_uploader.upload_short(
                        youtube, 
                        video_file, 
                        final_title, 
                        final_description, 
                        tags_list
                    )
                    
                    st.success(f"✅ Upload Complete!\n🎉 Successfully uploaded: {result['snippet']['title']}")
                    st.write(f"Video ID: {result['id']}")
                    st.write(f"Watch at: https://youtube.com/shorts/{result['id']}")
                    
                    # Cleanup
                    try:
                        os.remove(video_file)
                        st.session_state.downloaded_info = None # Reset state after successful upload
                        st.info("Temporary video file deleted.")
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"Failed to upload to YouTube: {e}")
