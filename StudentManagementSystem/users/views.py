from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_auth = openapi.Parameter(
    'Authorization', openapi.IN_HEADER, description="Bearer Token", type=openapi.TYPE_STRING
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[token_auth])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_auth])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
