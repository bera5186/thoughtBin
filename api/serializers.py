from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
