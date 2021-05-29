from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import date
# Create your views here.

@permission_classes([IsAuthenticated])
class ServerTime(APIView):

    def get(self, request):
        return Response(data=date.today(), status=status.HTTP_200_OK)