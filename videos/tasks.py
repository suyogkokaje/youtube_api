from googleapiclient.discovery import build
from datetime import datetime, timedelta
from .models import Video
from celery import shared_task
from api_key.models import ApiKey
from django.utils import timezone

def get_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def save_video_to_db(video_id, title, description, published_at, thumbnail_url):
    Video.objects.get_or_create(
        video_id=video_id,
        defaults={
            'title': title,
            'description': description,
            'published_at': published_at,
            'thumbnail_url': thumbnail_url,
        }
    )

def fetch_video_info(youtube, video_id):
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet,contentDetails'
    ).execute()

    video_info = video_response.get('items', [])[0]['snippet']
    return video_info

def process_search_result(search_result, youtube):
    video_id = search_result['id']['videoId']
    video_info = fetch_video_info(youtube, video_id)

    title = video_info['title']
    description = video_info['description']
    published_at = datetime.strptime(video_info['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    thumbnail_url = video_info['thumbnails']['default']['url']

    save_video_to_db(video_id, title, description, published_at, thumbnail_url)

def handle_exception(api_key_obj, e):
    if 'quotaExceeded' in str(e):
        print(f"Quota exceeded for API key: {api_key_obj.key}. Marking it as blacklisted.")
        api_key_obj.blacklisted = True
        api_key_obj.save()
    else:
        print("Following error occurred while saving the video to the db")
        print(e)

@shared_task
def fetch_and_store_youtube_videos():
    api_keys = ApiKey.objects.filter(blacklisted=False)

    if not api_keys.exists():
        print("No valid API keys available.")
        return

    for api_key_obj in api_keys:
        api_key = api_key_obj.key
        youtube = get_youtube_service(api_key)

        try:
            one_month_ago = timezone.now() - timedelta(days=30)

            search_response = youtube.search().list(
                q='python programming',
                type='video',
                part='id,snippet',
                maxResults=10,
                publishedAfter=one_month_ago.isoformat() + 'Z',
            ).execute()

            for search_result in search_response.get('items', []):
                process_search_result(search_result, youtube)

            print("Videos saved to the DB successfully")

        except Exception as e:
            handle_exception(api_key_obj, e)
