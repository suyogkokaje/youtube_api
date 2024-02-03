from django.http import JsonResponse
from googleapiclient.discovery import build
from datetime import datetime
from yt_api.utils import get_yt_api_key


def get_youtube_videos(request):
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

        videos = []

        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet,contentDetails'
            ).execute()

            video_info = video_response.get('items', [])[0]['snippet']

            title = video_info['title']
            description = video_info['description']
            publishing_datetime = datetime.strptime(video_info['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            thumbnail_url = video_info['thumbnails']['default']['url']

            videos.append({
                'title': title,
                'description': description,
                'publishing_datetime': publishing_datetime,
                'thumbnail_url': thumbnail_url,
            })

        return JsonResponse({'videos': videos})

    except Exception as e:
        return JsonResponse({'error': str(e)})
