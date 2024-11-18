from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains') 
    instructor = filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'instructor']
