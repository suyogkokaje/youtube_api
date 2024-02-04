from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Video
from .serializers import VideoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class VideoPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 100

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    @method_decorator(cache_page(60 * 15, cache='default'))
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter videos by start date (YYYY-MM-DD)'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter videos by end date (YYYY-MM-DD)'),
        ],
        responses={200: VideoSerializer(many=True)},
        operation_summary='List all videos with optional date range filtering.',
    )
    def list(self, request, *args, **kwargs):
        """

        - `page`: page number within the paginated result

        - `page_size`: number of results per page

        - `start_date`: start date of a range.

        - `end_date`: end date of a range.
        """
        try:
            queryset = Video.objects.all().order_by('-published_at')

            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            if start_date and end_date:
                queryset = queryset.filter(published_at__range=[start_date, end_date])

            self.queryset = queryset
            return super().list(request, *args, **kwargs)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
