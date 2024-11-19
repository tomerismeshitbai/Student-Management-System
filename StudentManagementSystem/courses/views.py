from rest_framework import viewsets
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilter
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    @method_decorator(cache_page(60*15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
def invalidate_course_cache(sender, instance, **kwargs):
    cache.delete("CourseViewSet_list")
    cache.delete(f"CourseViewSet_retrieve_{instance.pk}")

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
