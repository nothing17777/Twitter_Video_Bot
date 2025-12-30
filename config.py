import os
import tweepy
from dotenv import load_dotenv

# 1. Load the passwords from the .env file
load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN", "").strip()
api_key = os.getenv("API_KEY", "").strip()
api_secret = os.getenv("API_SECRET", "").strip()
access_token = os.getenv("ACCESS_TOKEN", "").strip()
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET", "").strip()

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True
)    

# 4. Set up the authentication for API (v1.1)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
v1_api = tweepy.API(auth, wait_on_rate_limit=True)

if __name__ == "__main__":
    rate_limits = v1_api.rate_limit_status()['resources']
    print(rate_limits)