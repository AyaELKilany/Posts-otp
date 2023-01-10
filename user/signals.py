
from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import User
import os
from posts_otp.settings import MEDIA_ROOT

 
 
@receiver(post_save, sender=User)
def update_img_path(sender, instance, created, **kwargs):
    if created:
        image = instance.profile_image
        path = image.path
        if not path:
            return
        print('signals old path : ' , path)
        filename = path.split('/')[5]
        print('signals old name : ' ,filename)
        new_path = os.path.join(MEDIA_ROOT , sender.get_image_path(instance,filename))
        if not os.path.exists(new_path):
            os.makedirs(os.path.dirname(new_path))
        os.rename(path , new_path)
        instance.profile_image.name = sender.get_image_path(instance,filename)
        instance.save
        
        
        
# @receiver(post_save, sender=Requests)
# def update_image_path(sender, instance, created,**kwargs):
#     if created:
#         attachfile=instance.attach
#         old_name=attachfile.name
#         if not old_name:
#             return 
#         new_name = os.path.basename(old_name)
#         new_path = os.path.join(settings.MEDIA_ROOT,sender.upload_to_attach(instance, new_name))
#         if not os.path.exists(new_path):
#             os.makedirs(os.path.dirname(new_path))
#         os.rename(attachfile.path, new_path)
#         instance.attach.name=sender.upload_to_attach(instance, new_name)
#         instance.save()