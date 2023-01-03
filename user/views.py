from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from .models import User
from .serializers import *
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny

@api_view(['POST'])
def create_User(request):
    data = request.data
    user = UserCreateSerializer(data=data)
    if user.is_valid():
        user.save()
        return Response({'User' : user.data} , status=status.HTTP_200_OK)
    return Response({'User' : user.errors} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_Users(request):
    if request.user.is_staff:
        Queryset = User.objects.all()
        serializer = UserSerializer(Queryset , many=True)
        return Response({'Users' : serializer.data} , status=status.HTTP_200_OK)
    raise PermissionError('Unauthorized , Only Staff')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_User(request , id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response({'User' : serializer.data} , status=status.HTTP_200_OK)
    except:
        raise ValueError('User not found')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_User(request):
    email = request.user.email
    user = User.objects.get(email=email)
    user_updated = UserCreateSerializer(user ,  data=request.data , partial=True)
    if user_updated.is_valid():
        user_updated.save()
        return Response({'response' : user_updated.data} , status=status.HTTP_200_OK)
    return Response({'response' : user_updated.errors} , status=status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_User(request , id):
    if request.user.is_staff:
        user = User.objects.get(id=id).delete()
        return Response({'message' : 'User deleted successfully'})
    return PermissionError('Unauthorized , Only Staff')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_Staff(request):
    if request.user.is_staff:
        Queryset= User.objects.filter(is_staff=True)
        serializer = UserSerializer(Queryset , many=True)
        return Response({'Staff' : serializer.data} , status=status.HTTP_200_OK)
    raise PermissionError('Unauthorized , Only Staff')

@api_view(['POST'])
def create_token(request):
    query_Set = VerificationOTP.objects.all().delete()
    data = request.data
    otp = OtpEmail(data=data)
    if otp.is_valid():
        otp.save()
        print('views token created' , otp.data)
        return Response({'message' : 'Email Sent'} , status=status.HTTP_200_OK)
    return Response({'message' : otp.errors} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_token(request):
    token = verify_token(data=request.data)