from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('students.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('grades.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('notifications.urls')),
]
