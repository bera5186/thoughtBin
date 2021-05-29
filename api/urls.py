from django.urls import path
from .views import  ServerTime
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('servertime', ServerTime.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)