import os
from dotenv import load_dotenv

load_dotenv()

def get_yt_api_key():
    api_key = os.getenv('YOUTUBE_API_KEY')

    if api_key is None:
        raise ValueError("YouTube API key not found in the .env file.")

    return api_key
