import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
import random

load_dotenv()

#Video Titles
titles = [
    "this cat is ai",
    "ai cats are wild",
    "this cat does not exist",
    "ai made this cat",
    "you won’t believe this is ai",
    "this ai cat feels unreal",
    "ai cats are evolving",
    "real or ai?",
    "this cat is not normal",
    "ai cat moment",
    "this cat broke my brain",
    "ai cats are getting better",
    "this cat feels illegal",
    "something is off about this cat",
    "ai really made this",
    "this cat is too perfect",
    "ai cats hit different",
    "this cat isn’t real right?",
    "ai created this cat",
    "this cat is from another universe",
    "ai cat vibes",
    "this cat looks real",
    "ai cats are unstoppable",
    "this cat scares me",
    "ai cat energy",
    "this shouldn’t be possible",
    "this cat feels cinematic",
    "ai cat core",
    "this cat knows something",
    "ai cats just won"
]
titles = [i.capitalize() for i in titles]

# Load credentials from .env
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

TOKEN_FILE = 'token.pickle'

def get_authenticated_service():
    """
    Authenticate and return YouTube service object
    """
    credentials = None
    
    # Check if token file exists (for reusing credentials)
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # Refresh expired credentials
            credentials.refresh(Request())
        else:
            # Create credentials dictionary from .env
            client_config = {
                "installed": {
                    "client_id": YOUTUBE_CLIENT_ID,  # Use the loaded variable
                    "client_secret": YOUTUBE_CLIENT_SECRET,  # Use the loaded variable
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            
            # Run OAuth flow
            flow = InstalledAppFlow.from_client_config(
                client_config,
                SCOPES
            )
            credentials = flow.run_local_server(port=8080)
        
        # Save credentials for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)
    
    # Build and return YouTube service
    return build('youtube', 'v3', credentials=credentials)

def upload_short(youtube, video_file, title, description, tags=None):
    """
    Upload a YouTube Short
    
    Args:
        youtube: Authenticated YouTube service object
        video_file: Path to the video file
        title: Video title
        description: Video description (include #Shorts)
        tags: List of tags (optional)
    """
    
    # Video metadata
    body = {
        'snippet': {
            'title': title,
            'description': description + '\n\n#Shorts',  # Add #Shorts tag
            'tags': tags or ['shorts', 'short video'],
            'categoryId': '22'  # People & Blogs category
        },
        'status': {
            'privacyStatus': 'public',  # 'public', 'private', or 'unlisted'
            'selfDeclaredMadeForKids': False,
        }
    }
    
    # Create media upload object
    media = MediaFileUpload(
        video_file,
        chunksize=-1,  # Upload in a single request
        resumable=True,
        mimetype='video/*'
    )
    
    # Execute upload
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    print(f'Uploading: {video_file}')
    print('Please wait...\n')
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f'Upload Progress: {progress}%')
    
    print('\n✅ Upload Complete!')
    print(f"Video ID: {response['id']}")
    print(f"Watch at: https://youtube.com/shorts/{response['id']}")
    
    return response


def main():
    """
    Main function to upload a short
    """
    try:
        # Get authenticated YouTube service
        youtube = get_authenticated_service()
        
        # Video details
        tags = ['shorts', 'trending', 'viral', 'funnycat', 'aicat', 'aistory', 'trending']
        hashtags = '#Shorts #Trending #Viral #Funnycat #AICat #AIStory #Trending'
        
        video_file = 'downloads/catMeme1.mp4'  # Your video file path
        title = random.choice(titles) + '#Funnycat #AICat #AIStory #Viral #Shorts #Trending'
        description = hashtags + "\nAI-generated cat 🐱\nScroll if you dare."
        
        # Upload the video
        result = upload_short(youtube, video_file, title, description, tags)
        
        print(f"\n🎉 Successfully uploaded: {result['snippet']['title']}")
        
    except Exception as e:
        print(f'❌ An error occurred: {e}')


if __name__ == '__main__':
    main()