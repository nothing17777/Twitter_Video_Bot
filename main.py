import config
import youtube_downloader
import os
import time

def post_video_tweet():
    print(f"Starting specific video tweet process...")
    
    # 1. Download specific video
    target_url = "https://www.youtube.com/watch?v=-JA7xANgNMU"
    video_path, title = youtube_downloader.download_video_direct(target_url)
    
    if not video_path:
        print("Failed to download video. Aborting.")
        return

    print(f"Video ready at: {video_path}")
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
        # User requested title as text
        tweet_text = f"{title}"
        response = config.client.create_tweet(text=tweet_text, media_ids=[media_id])
        print(f"Tweeted successfully! ID: {response.data['id']}")

    except Exception as e:
        print(f"Error during Twitter interactions: {e}")

    finally:
        # 4. Cleanup
        if os.path.exists(video_path):
            print(f"Cleaning up file: {video_path}")
            os.remove(video_path)

if __name__ == "__main__":
    post_video_tweet()