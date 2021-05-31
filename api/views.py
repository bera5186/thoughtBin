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
import math


@permission_classes([IsAuthenticated])
class ServerTime(APIView):
    def get(self, request):
        return Response(data=date.today(), status=status.HTTP_200_OK)


# @permission_classes([IsAuthenticated])
# class Post_CRUD(APIView):
#     """
#         Post Crud endpoints
#
#     """
#     def get(self, request):
#
#         context = {"error": True}
#
#         post_id = request.GET.get("id")
#
#         # check if post is
#         if post_id is None:
#             context["message"] = "Id in query is required"
#             return Response(context, status=status.HTTP_400_BAD_REQUEST)
#
#         if not is_uuid(post_id):
#             context["message"] = "Id should be a valid UUID"
#             return Response(context, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             post = Post.objects.get(id=post_id)
#             serializer = PostSerializer(post, many=False)
#             context["error"] = False
#             context["result"] = serializer.data
#             return Response(context, status=status.HTTP_200_OK)
#         except Post.DoesNotExist:
#             post = None
#             context["result"] = post
#             return Response(context, status=status.HTTP_404_NOT_FOUND)


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

        context = {"error": True}

        try:
            clap_count = request.data["clap_count"]
        except KeyError:
            context["message"] = "clap_count is not present in body"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if type(clap_count) != int or clap_count < 1:
            context["message"] = "clap_count should be an integer greater than 0"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


        user = UserCreateSerializer(request.user).data
        print(pk)
        print(type(user["email"]))
        print(type(pk))
        clap_post.delay(user["email"], str(pk), clap_count)

        context["error"] = False

        return Response(context, status=status.HTTP_200_OK)
