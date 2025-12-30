import streamlit as st
from downloader import youtube_downloader
import random
import config
import os
import time
from format import format

# Initialize session state for tracking used video URLs
if 'video_urls' not in st.session_state:
    st.session_state.video_urls = set()
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = None
if 'selected_comment' not in st.session_state:
    st.session_state.selected_comment = None

st.title("Random Video Selector")

st.write("Search for videos and get a random one that hasn't been used yet")

with st.container(border=True):
    col1, col2 = st.columns([0.8, 0.2], vertical_alignment='bottom')
    with col1:
        query = st.text_input("Video Keywords")
    with col2:
        search_button = st.button("Get Random Video", width='stretch')

if search_button and query:
    with st.spinner("Searching for videos..."):
        videos = youtube_downloader.searchVideosUnderTwoMin(query)
        
        if not videos:
            st.error("No videos found for this query!")
        else:
            # Filter out videos that are already in the set
            unused_videos = [v for v in videos if v.get('url') not in st.session_state.video_urls]
            
            if not unused_videos:
                st.warning(f"❌ All videos from this query have already been used. Query not accepted.")
                st.info(f"Used videos count: {len(st.session_state.video_urls)}")
            else:
                # Select a random video from unused ones
                selected_video = random.choice(unused_videos)
                video_url = selected_video.get('url')
                
                # Add to the set
                st.session_state.video_urls.add(video_url)
                
                # Store in session state
                st.session_state.selected_video = selected_video
                
                # Get random top comment
                with st.spinner("Loading top comments..."):
                    comments = youtube_downloader.get_top_comments(video_url)
                    
                    if comments:
                        st.session_state.selected_comment = random.choice(comments)
                    else:
                        st.session_state.selected_comment = None

# Display selected video if exists
if st.session_state.selected_video:
    selected_video = st.session_state.selected_video
    video_url = selected_video.get('url')
    
    st.success(f"✅ Selected video! (Total used: {len(st.session_state.video_urls)})")
    
    # Display video info
    with st.container(border=True):
        st.subheader(selected_video.get('title', 'Unknown Title'))
        
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            if selected_video.get('thumbnails'):
                st.image(selected_video['thumbnails'][0]['url'])
        
        with col2:
            st.write(f"**Duration:** {selected_video.get('duration', 0)} seconds")
            st.write(f"**Author:** {selected_video.get('uploader', 'Unknown')}")
            st.write(f"**Views:** {selected_video.get('view_count', 0):,}")
            st.write(f"**URL:** {video_url}")
    
    #HashTags
    st.write(format.hashtag_from_query(query))
    # Display random comment
    if st.session_state.selected_comment:
        st.info(f"**Random Top Comment:** {st.session_state.selected_comment}")
    else:
        st.warning("No suitable comments found for this video")
    
    # Twitter posting section
    st.divider()
    st.subheader("📤 Post to Twitter")
    
    # Generate hashtags from the query
    hashtags = " ".join(format.hashtag_from_query(query))
    default_text = f"{st.session_state.selected_comment or selected_video.get('title', '')}\n\n{hashtags}"
    
    tweet_text = st.text_area(
        "Tweet Text", 
        value=default_text,
        max_chars=280,
        help="Edit the text that will be posted with the video"
    )
    
    if st.button("🐦 Post to Twitter", type="primary"):
        with st.spinner("Downloading video..."):
            video_path, title = youtube_downloader.download_video_direct(video_url)
            
        if not video_path:
            st.error("❌ Failed to download video")
        else:
            try:
                with st.spinner("Uploading to Twitter..."):
                    # Upload video with chunked upload
                    media = config.v1_api.media_upload(video_path, media_category='tweet_video', chunked=True)
                    media_id = media.media_id
                    st.write(f"✅ Media uploaded! ID: {media_id}")
                    
                    # Wait for processing
                    if hasattr(media, 'processing_info'):
                        info = media.processing_info
                        state = info.get('state')
                        st.write(f"Media processing status: {state}")
                        
                        while state in ['pending', 'in_progress']:
                            check_after_secs = info.get('check_after_secs', 5)
                            st.write(f"Waiting {check_after_secs} seconds to check status...")
                            time.sleep(check_after_secs)
                            
                            status = config.v1_api.get_media_upload_status(media_id)
                            info = status.processing_info
                            state = info.get('state')
                            st.write(f"Media processing status: {state}")
                            
                        if state == 'failed':
                            st.error("❌ Media processing failed!")
                            st.stop()  # Stop here, don't try to post
                        
                        if state == 'succeeded':
                            st.success("✅ Media processing succeeded!")
                    else:
                        # No processing info - wait for safety
                        st.write("No processing info returned. Waiting 5s for safety...")
                        time.sleep(5)
                    
                with st.spinner("Posting tweet..."):
                    response = config.client.create_tweet(text=tweet_text, media_ids=[media_id])
                    tweet_id = response.data['id']
                    st.success(f"✅ Tweet posted successfully!")
                    youtube_downloader.add_used_video(video_url)
                    st.write(f"Tweet ID: {tweet_id}")
                    st.write(f"View at: https://twitter.com/user/status/{tweet_id}")
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                # Cleanup
                if os.path.exists(video_path):
                    os.remove(video_path)
                    st.write("🧹 Cleaned up downloaded file")

# Show current stats
with st.sidebar:
    st.header("Statistics")
    st.metric("Total Videos Used", youtube_downloader.get_used_videos_count())
    if st.button("Clear History"):
        youtube_downloader.clear_used_videos()
        st.session_state.selected_video = None
        st.session_state.selected_comment = None
        st.rerun()