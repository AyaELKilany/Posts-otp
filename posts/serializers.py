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
        user = validated_data.pop('user')
        post = validated_data.pop('post')
        post = Post.objects.create_post(user=user , post=post , **validated_data)
        post.save()
        return post