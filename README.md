# 📺 Twitter Video Bot

A sophisticated Streamlit-based application designed to search for anime clips on YouTube, extract top comments, and post them directly to Twitter with automated hashtag generation and duplicate prevention.

## ✨ Features

- **YouTube Search**: Find videos under 2 minutes based on keywords.
- **Comment Extraction**: Automatically pulls the top liked comments from YouTube to use as tweet content.
- **Random Selector**: Pick a random unused video from search results for quick posting.
- **Smart Hashtags**: Automatic hashtag generation based on anime titles (Chainsaw Man, JJK, One Piece, etc.).
- **Duplicate Prevention**: Keeps track of every video posted in `usedVideo.txt` to ensure you never post the same clip twice.
- **Premium UI**: Clean, responsive interface built with Streamlit.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- **FFmpeg**: Required for video processing.
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- Twitter Developer Account (API Keys)

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

3. Configure environment variables:
   - Copy `.env_example` to `.env`
   - Fill in your Twitter API credentials.

### Running the App

```bash
streamlit run app.py
```

## 🛠️ Technology Stack

- **Streamlit**: Frontend UI
- **yt-dlp**: YouTube metadata and video downloading
- **Tweepy**: Twitter API integration
- **FFmpeg**: Video encoding for Twitter compatibility

## 📂 Project Structure

- `app.py`: Main entry point and navigation.
- `pages/search.py`: Manual video search and history management.
- `pages/randomVideo.py`: Random video selection and posting logic.
- `youtube_downloader.py`: Core logic for YT interaction.
- `format.py`: Hashtag and text formatting utilities.
- `usedVideo.txt`: Local database of posted URLs.
