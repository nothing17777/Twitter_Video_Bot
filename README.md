# 📺 Social Video Bot

A sophisticated Streamlit-based application designed to manage video content across YouTube, TikTok, and Twitter. Search for anime clips, download TikToks, and automate posting with smart formatting.

## ✨ Features

- **YouTube search & Tweet**: Find YouTube videos under 2 minutes, extract top comments, and post them directly to Twitter with automated hashtag generation.
- **TikTok Downloader**: Download TikTok videos directly by URL.
- **YouTube Shorts Uploader**: Upload downloaded videos (like TikToks) as YouTube Shorts with customizable titles, descriptions, and tags.
- **Smart Hashtags**: Automatic hashtag generation for anime clips (Chainsaw Man, JJK, One Piece, etc.).
- **Duplicate Prevention**: Tracks posted videos in `usedVideo.txt` to ensure no double-posting on Twitter.
- **Premium UI**: Clean, responsive interface built with Streamlit.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- **FFmpeg**: Required for video processing and encoding.
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- Twitter Developer Account (for Twitter posting)
- Google Cloud Project with YouTube Data API v3 enabled (for YouTube uploading)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nothing17777/Twitter_Video_Bot.git
   cd Twitter_Video_Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (`.env`):
   - `BEARER_TOKEN`, `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET` (Twitter)
   - `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET` (YouTube API)

### Running the App

```bash
streamlit run app.py
```

## 🛠️ Technology Stack

- **Streamlit**: Frontend UI
- **yt-dlp**: YouTube and TikTok downloading
- **Tweepy**: Twitter API integration
- **Google API Client**: YouTube Data API integration
- **FFmpeg**: Video encoding for platform compatibility

## 📂 Project Structure

- `app.py`: Main entry point and navigation.
- `downloader/`: Core logic for YouTube and TikTok interaction.
- `uploader/`: YouTube Shorts upload implementation.
- `posters/`: Twitter posting automation.
- `format/`: Hashtag and text formatting utilities.
- `pages/`: Streamlit UI pages (Search, Random Video, TikTok).
- `usedVideo.txt`: Local database of posted URLs.
