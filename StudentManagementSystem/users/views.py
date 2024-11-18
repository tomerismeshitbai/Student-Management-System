from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60*15), name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
