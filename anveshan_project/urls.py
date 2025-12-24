"""
URL configuration for anveshan_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('soil_moisture.urls')),
]

