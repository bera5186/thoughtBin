from django.urls import path, include
from authMiddleware import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
