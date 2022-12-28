from django.db import models
from user.models import User

class PostManager(models.Manager):
    def get_published(self):
        return super().get_queryset().filter(is_published=True)
    
    def get_unpublished(self):
        return super.get_queryset().filter(is_published=False)
            

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='posts')
    post = models.CharField(max_length=1000)
    topic = models.CharField(max_length=30)
    likes = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    objects = PostManager()
    
