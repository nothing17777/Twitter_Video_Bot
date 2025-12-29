import config
import youtube_downloader
import random
import os
import time
import argparse

# File to store used video URLs
USED_VIDEOS_FILE = "used_videos.txt"

# Curated list of popular anime search terms
ANIME_SEARCH_TERMS = [
    "Jujutsu Kaisen epic moments",
    "One Piece best fights",
    "Demon Slayer animation peaks",
    "Attack on Titan intense scenes",
    "Naruto Shippuden emotional moments",
    "Bleach Thousand-Year Blood War clips",
    "Chainsaw Man action scenes",
    "Dragon Ball Super hype moments",
    "Hunter x Hunter best scenes",
    "Mob Psycho 100 animation",
    "My Hero Academia hype scenes",
    "Solo Leveling best moments",
    "Vinland Saga intense scenes"
]

def load_used_videos():
    if os.path.exists(USED_VIDEOS_FILE):
        with open(USED_VIDEOS_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_used_video(url):
    with open(USED_VIDEOS_FILE, "a") as f:
        f.write(f"{url}\n")

def run_bot(query):
    print(f"--- Starting Video Bot Automation ---")
    print(f"Query: {query}")
    
    used_urls = load_used_videos()
    
    print("Searching for videos...")
    videos = youtube_downloader.searchVideosUnderTwoMin(query)
    
    if not videos:
        print("No videos found for this query!")
        return
    
    # Filter out used videos
    unused_videos = [v for v in videos if v.get('url') not in used_urls]
    
    if not unused_videos:
        print(f"All videos from this query ({query}) have already been used.")
        return
    
    # Select random video
    selected_video = random.choice(unused_videos)
    video_url = selected_video.get('url')
    title = selected_video.get('title', 'Unknown')
    
    print(f"Selected video: {title} ({video_url})")
    
    # Get random top comment
    print("Fetching top comments...")
    comments = youtube_downloader.get_top_comments(video_url)
    
    tweet_text = ""
    if comments:
        tweet_text = random.choice(comments)
        print(f"Selected comment: {tweet_text}")
    else:
        tweet_text = title
        print(f"No comments found, using title as tweet text: {tweet_text}")
    
    # Download video
    print("Downloading video (direct)...")
    video_path, _ = youtube_downloader.download_video_direct(video_url)
    
    if not video_path:
        print("Failed to download video!")
        return
    
    try:
        print("Uploading to Twitter (chunked)...")
        media = config.v1_api.media_upload(video_path, media_category='tweet_video', chunked=True)
        media_id = media.media_id
        
        # Poll for processing
        if hasattr(media, 'processing_info'):
            info = media.processing_info
            state = info.get('state')
            
            while state in ['pending', 'in_progress']:
                check_after_secs = info.get('check_after_secs', 5)
                print(f"Processing ({state})... waiting {check_after_secs}s")
                time.sleep(check_after_secs)
                
                status = config.v1_api.get_media_upload_status(media_id)
                info = status.processing_info
                state = info.get('state')
            
            if state == 'failed':
                print("Media processing failed!")
                return
            
            print("Media processing succeeded!")
        else:
            print("No processing info, waiting 5s for safety...")
            time.sleep(5)
            
        print("Posting tweet...")
        response = config.client.create_tweet(text=tweet_text, media_ids=[media_id])
        tweet_id = response.data['id']
        print(f"Successfully tweeted! ID: {tweet_id}")
        
        # Save to used list only on success
        save_used_video(video_url)
        
    except Exception as e:
        print(f"Error during posting: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
            print("Cleaned up video file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter Video Bot Automation")
    parser.add_argument("query", nargs="?", help="Search query for YouTube videos (optional)")
    args = parser.parse_args()
    
    query = args.query
    if not query:
        query = random.choice(ANIME_SEARCH_TERMS)
        print(f"No query provided. Selecting random anime term: {query}")
    
    run_bot(query)
