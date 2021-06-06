from django.core import paginator
from django.db import transaction

from .tasks import clap_post

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from authMiddleware.models import UserEncoder
from authMiddleware.serializers import UserCreateSerializer

from .models import *
from .serializers import *
from .helpers import is_uuid
from datetime import date


class ServerTime(APIView):
    def get(self, request):
        return Response(data=date.today(), status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class PostsCRUD(viewsets.ViewSet):
    """
    Posts CRUD endpoints

    """

    def list(self, request):
        """
        Get All Posts with pagination
        """

        context = {"error": False}

        limit = request.GET.get("limit")
        offset = request.GET.get("offset")

        if limit is None or int(limit) <= 0:
            limit = 10
        if offset is None or int(offset) < 1:
            offset = 1

        posts = Post.objects.all().order_by("created_at")

        total_results = posts.count()
        n_pages = math.ceil(total_results / int(limit))

        posts_limited = paginator.Paginator(posts, limit)
        posts_offseted = posts_limited.get_page(offset)
        serialized_posts = PostSerializer(posts_offseted, many=True)

        context["total"] = total_results
        context["pages"] = n_pages
        context["results"] = serialized_posts.data

        return Response(context, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST", "GET"])
    def clap(self, request, pk):
        """
        Runs a celery task to like post
        """

        context = {"error": True}

        try:
            clap_count = request.data["clap_count"]
        except KeyError:
            context["message"] = "clap_count is not present in body"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if type(clap_count) != int or clap_count < 1:
            context["message"] = "clap_count should be an integer greater than 0"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not is_uuid(pk):
            context["message"] = "Invalid PostId"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = UserCreateSerializer(request.user).data
        clap_post.delay(user["email"], str(pk), clap_count)

        context["error"] = False

        return Response(context, status=status.HTTP_200_OK)
