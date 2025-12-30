import time
import logging
from main import post_video_tweet

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_scheduler.log"),
        logging.StreamHandler()
    ]
)

INTERVAL = 2 * 60 * 60  # 2 hours in seconds

def run_scheduler():
    logging.info("Bot Scheduler started. Will post every 2 hours.")
    
    while True:
        try:
            logging.info("Triggering post_video_tweet()...")
            post_video_tweet()
            logging.info(f"Task completed. Sleeping for {INTERVAL/3600} hours...")
        except Exception as e:
            logging.error(f"Error in scheduler loop: {e}")
            logging.info("Retrying in 60 seconds...")
            time.sleep(60)
            continue
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_scheduler()
