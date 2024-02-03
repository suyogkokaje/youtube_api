from googleapiclient.discovery import build
from datetime import datetime
from .models import Video
from yt_api.utils import get_yt_api_key
from celery import shared_task

def save_video_to_db(video_id, title, description, published_at, thumbnail_url):
    video, created = Video.objects.get_or_create(
        video_id=video_id,
        defaults={
            'title': title,
            'description': description,
            'published_at': published_at,
            'thumbnail_url': thumbnail_url,
        }
    )

    if not created:
        video.title = title
        video.description = description
        video.published_at = published_at
        video.thumbnail_url = thumbnail_url
        video.save()

@shared_task
def fetch_and_store_youtube_videos():
    api_key = get_yt_api_key()
    query = 'python programming'

    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=10 
        ).execute()

        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet,contentDetails'
            ).execute()

            video_info = video_response.get('items', [])[0]['snippet']

            title = video_info['title']
            description = video_info['description']
            published_at = datetime.strptime(video_info['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            thumbnail_url = video_info['thumbnails']['default']['url']

            save_video_to_db(video_id, title, description, published_at, thumbnail_url)

        print("Videos saved to the DB successfully")

    except Exception as e:
        print("Following error occurred while saving the video to the db")
        print(e)
