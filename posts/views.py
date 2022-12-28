from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['POST'])
def create_post(request):
    post = PostSerializer(data = request.data)
    if post.is_valid():
        return Response({'Post': post.data} , status=status.HTTP_200_OK)
    
    return Response({'Post': post.errors} , status=status.HTTP_400_BAD_REQUEST)