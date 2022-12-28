from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,mobile,email,password , **other_fields):
        if not mobile:
            raise ValueError(_('you must provide a mobile number'))
        if not email:
            raise ValueError(_('you must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(mobile=mobile, email=email , **other_fields)
        user.set_password(password)
        user.save()
        return user
    
        
    def create_staff(self,mobile,email,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('staff must have is_staff=True.'))
        
        self.create_user(mobile,email,password,**other_fields)
         


class User(AbstractBaseUser , PermissionsMixin):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(max_length=80 , unique=True)
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    

