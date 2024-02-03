from rest_framework import viewsets
from rest_framework.response import Response
from .models import ApiKey
from .serializers import ApiKeySerializer

class ApiKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
