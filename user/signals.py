
from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import User
import os

 
 
@receiver(post_save, sender=User)
def update_img_path(sender, instance, created, **kwargs):
    if created:
        path = instance.profile_image.path
        filename = path.split('/')[3]
        new_path = f'app/profile_images/user{instance.id}_{filename}'
        print(new_path)
        os.rename(src=path , dest=new_path)