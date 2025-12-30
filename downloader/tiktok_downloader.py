import yt_dlp
import os

def download_tiktok_video(url, output_path='downloads'):
    """
    Download a TikTok video using yt-dlp.
    
    Args:
        url (str): The TikTok video URL
        output_path (str): Directory to save the video (default: 'downloads')
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    # Video Path Initialization
    video_filename = f"{'catMemeVideo'}.mp4" 
    output_path = os.path.join(output_path, video_filename)
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except:
            pass

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Downloading TikTok video from: {url}")
            ydl.download([url])
            print("Download completed successfully!")
            return info
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Replace with your TikTok video URL
    video_url = "https://www.tiktok.com/@video_aicat/video/7579308392280362262"
    download_tiktok_video(video_url)