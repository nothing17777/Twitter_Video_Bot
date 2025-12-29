import yt_dlp
import os

def searchVideosUnderTwoMin(query, limit=5, max_duration_seconds=120):
    """
    Search for videos under a given duration limit.
    
    Args:
        query: Search query
        limit: Maximum number of videos to return (default: 5)
        max_duration_seconds: Maximum video duration in seconds (default: 120)
    
    Returns:
        List of video entries
    """
    search_limit = limit * 3
    
    search_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'default_search': f'ytsearch{search_limit}',
        'noplaylist': True,
    }
    
    entries = []
    with yt_dlp.YoutubeDL(search_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch{search_limit}:{query}", download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    # Only add videos under the duration limit
                    if entry.get('duration') and entry.get('duration') < max_duration_seconds:
                        entries.append(entry)
                        # Stop once we have enough videos
                        if len(entries) >= limit:
                            break
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    return entries


def get_top_comments(video_url, max_comments=10, max_length=150):
    """

    Extract top comments (sorted by likes) from a YouTube video that are under max_length characters.
    Filters out comments containing timestamps, questions, links, and non-English text.
    
    Args:
        video_url: YouTube video URL
        max_comments: Maximum number of comments to return (default: 10)
        max_length: Maximum character length for comments (default: 150)
    
    Returns:
        List of comment strings

    """
    import re
    
    # Pattern to detect timestamps like 0:00, 1:23, 12:34:56, etc.
    timestamp_pattern = r'\d{1,2}:\d{2}(?::\d{2})?'
    
    # Pattern to detect questions (what, why, how, or ?)
    question_pattern = r'\b(what|why|how)\b|\?'
    
    # Pattern to detect URLs/links (including shortened URLs like got.cr/abc)
    url_pattern = r'http[s]?://|www\.|\.(com|net|org|io|cr|ly|gl)/|\w+\.\w+/'
    
    def is_likely_english(text):
        """Check if text is likely English using basic heuristics"""
        # Count ASCII alphabetic characters
        ascii_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())
        
        # If no alphabetic characters, reject
        if total_chars == 0:
            return False
        
        # If more than 90% of alphabetic chars are ASCII, likely English
        return (ascii_chars / total_chars) > 0.9
    
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'getcomments': True,
    }
    
    comments = []
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if 'comments' in info and info['comments']:
                # Sort comments by like_count (descending) to get top comments
                sorted_comments = sorted(
                    info['comments'], 
                    key=lambda x: x.get('like_count', 0), 
                    reverse=True
                )
                
                for comment_data in sorted_comments:
                    comment_text = comment_data.get('text', '')
                    # Filter by length, timestamps, questions, URLs, and language
                    if (comment_text and 
                        len(comment_text) <= max_length and 
                        not re.search(timestamp_pattern, comment_text) and
                        not re.search(question_pattern, comment_text, re.IGNORECASE) and
                        not re.search(url_pattern, comment_text, re.IGNORECASE) and
                        is_likely_english(comment_text)):
                        comments.append(comment_text)
                        if len(comments) >= max_comments:
                            break
    except Exception as e:
        print(f"Error extracting comments: {e}")
    
    return comments



def download_video_direct(url):
    """

    Download a video from a direct URL.
    
    Args:
        url: URL of the video to download
    
    Returns:
        Tuple of (video_path, title) if successful, None if failed

    """
    print(f"Downloading direct URL: {url}")
    
    # Get info first to get clean title
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        try:
             info = ydl.extract_info(url, download=False)
             title = info.get('title', 'video')
             print(f"Title found: {title}")
        except:
             title = "downloaded_video"

    current_dir = os.getcwd()
    video_filename = f"{title}.mp4" 
    # Sanitize filename
    video_filename = "".join([c for c in video_filename if c.isalpha() or c.isdigit() or c==' ' or c=='.']).rstrip()
    if not video_filename.endswith(".mp4"):
        video_filename += ".mp4"
    
    output_path = os.path.join(current_dir, video_filename)
    
    # Clean up previous download if exists
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except:
            pass

    # Use specific options for this download
    # Twitter requires: H.264 video codec, AAC audio codec, MP4 container
    download_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }, {
            'key': 'FFmpegVideoRemuxer',
            'preferedformat': 'mp4',
        }],
        # Ensure we get Twitter-compatible codecs
        'postprocessor_args': [
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-b:a', '128k',
            '-movflags', '+faststart'
        ],
    }
    
    try:
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
             return output_path, title
        else:
             print("Download finished but file not found.")
             return None, None

    except Exception as e:
        print(f"Download error: {e}")
        return None, None

if __name__ == "__main__":
    download_video_direct("https://www.youtube.com/watch?v=ocBJ-lao81o")