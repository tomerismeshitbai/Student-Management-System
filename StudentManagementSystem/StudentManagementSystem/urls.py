from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication


schema_view = get_schema_view(
   openapi.Info(
      title="My Project API",
      default_version='v1',
      description="API documentation for My Project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   authentication_classes=[TokenAuthentication],
   
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('students.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('grades.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('notifications.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
]
