from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
    def create(self , validated_data):
        post = Post.objects.create(validated_data)
        post.save()
        return post