from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Video
from .serializers import VideoSerializer

class VideoPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 100

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    @method_decorator(cache_page(60 * 15, cache='default'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
