from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from .models import User
from .serializers import UserSerializer
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def all_Users(request):
    Queryset = User.objects.all()
    serializer = UserSerializer(Queryset , many=True)
    return Response({'Users' : serializer.data} , status=status.HTTP_200_OK)
    
