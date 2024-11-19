from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import StudentFilter
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    @method_decorator(cache_page(60*15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @method_decorator(cache_page(60*15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

@receiver(post_save, sender=Student)
@receiver(post_delete, sender=Student)

def invalidate_student_cache(sender, instance, **kwargs):
    cache.delete(f"student_profile_{instance.pk}")
    cache.delete("students_list")

