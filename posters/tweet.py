try:
    import config
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import config

from downloader import youtube_downloader
import os
import time
import random
from format import format

querys = ["chainsaw man clips", "bocchi the rock clips", "k-on clips", "jjk clips"]

query = random.choice(querys)

def post_video_tweet():
    print(f"Starting specific video tweet process...")
    
    # 1. Search and filter videos
    print(f"Searching for videos for query: {query}")
    videos = youtube_downloader.searchVideosUnderTwoMin(query)
    
    if not videos:
        print("No videos found for this query!")
        return

    # Filter out already used videos
    used_videos = youtube_downloader.get_used_videos()
    unused_videos = [v for v in videos if v.get('url') not in used_videos]

    if not unused_videos:
        print("All found videos have already been used.")
        return

    # 2. Select a random unused video
    video = random.choice(unused_videos)
    target_url = video.get('url')
    print(f"Selected video: {video.get('title')}")
    print(f"Selected video url: {target_url}")

    # 3. Get random top comment
    print("Fetching top comments...")
    comments = youtube_downloader.get_top_comments(target_url)
    selected_comment = random.choice(comments) if comments else None
    
    # 4. Prepare tweet text and hashtags
    hashtags_list = format.hashtag_from_query(query)
    hashtags = " ".join(hashtags_list)
    print(f"Hashtags: {hashtags}")

    # 5. Download video
    video_path, title = youtube_downloader.download_video_direct(target_url)
    
    if not video_path:
        print("Failed to download video. Aborting.")
        return
    print(f"Video ready at: {video_path}")

    if not title:
        title = "downloaded_video"
    print(f"Title: {title}")

    try:
        # 2. Upload Video (v1.1 API) - CHUNKED UPLOAD
        print("Uploading media (chunked)...")
        media = config.v1_api.media_upload(video_path, media_category='tweet_video', chunked=True)
        media_id = media.media_id
        print(f"Media uploaded! ID: {media_id}")
        
        # Wait for processing
        if hasattr(media, 'processing_info'):
            info = media.processing_info
            state = info.get('state')
            print(f"Media processing status: {state}")
            
            while state in ['pending', 'in_progress']:
                check_after_secs = info.get('check_after_secs', 5)
                print(f"Waiting {check_after_secs} seconds to check status...")
                time.sleep(check_after_secs)
                
                status = config.v1_api.get_media_upload_status(media_id)
                info = status.processing_info
                state = info.get('state')
                print(f"Media processing status: {state}")
                
            if state == 'failed':
                print("Media processing failed!")
                return
            
            if state == 'succeeded':
                print("Media processing succeeded!")
        else:
            # Sometimes explicit processing check is needed if 'processing_info' isn't in the initial response
            # but usually for tweet_video it is. 
            # We can force a wait just in case or assume it's small enough.
            print("No processing info returned. Waiting 5s for safety...")
            time.sleep(5)

        # 3. Post Tweet (v2 API)
        print("Posting tweet...")
        
        # Build tweet text: comment (or title) + hashtags
        base_text = selected_comment if selected_comment else title
        tweet_text = f"{base_text}\n\n{hashtags}"
        
        # Ensure tweet text doesn't exceed 280 characters
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."

        response = config.client.create_tweet(text=tweet_text, media_ids=[media_id])
        print(f"Tweeted successfully! ID: {response.data['id']}")
        
        # Mark as used after successful post
        youtube_downloader.add_used_video(target_url)
        print("Video marked as used.")

    except Exception as e:
        print(f"Error during Twitter interactions: {e}")

    finally:
        # 4. Cleanup
        if os.path.exists(video_path):
            print(f"Cleaning up file: {video_path}")
            os.remove(video_path)

if __name__ == "__main__":
    post_video_tweet()