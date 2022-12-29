from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    post = PostCreateSerializer(data=request.data)
    if post.is_valid():
        post.save()
        return Response({'Post': post.data} , status=status.HTTP_200_OK)
    return Response({'Post': post.errors} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):
    if request.user.is_staff:
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset , many=True)
        return Response({'AllPosts': serializer.data} , status=status.HTTP_200_OK)
    raise PermissionError('Unauthorized')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_published_posts(request):
    queryset = Post.objects.get_published()
    serializer = PostSerializer(queryset , many=True)
    return Response({'AllPosts': serializer.data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_unpublished_posts(request):
    if request.user.is_staff:
        queryset = Post.objects.get_unpublished()
        serializer = PostSerializer(queryset , many=True)
        return Response({'AllPosts': serializer.data} , status=status.HTTP_200_OK)
    raise PermissionError('Unauthorized')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request , id):
    post = Post.objects.get(id=id)
    updated_post = PostCreateSerializer(data=request.data , instance=post , partial=True)
    if updated_post.is_valid():
        updated_post.save()
        return Response({'message': updated_post.data} , status=status.HTTP_200_OK)
    return Response({'message': updated_post.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request , id):
    post = Post.objects.get(id=id).delete()
    return Response({'message' : 'Post deleted successfully'})