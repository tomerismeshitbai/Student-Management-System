from rest_framework import viewsets
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilter
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60*15), name='dispatch')
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

@method_decorator(cache_page(60*15), name='dispatch')
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
