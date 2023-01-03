from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django_otp.oath import TOTP
from django_otp.util import random_hex , hex_validator
import time
from django.core.mail import send_mail

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
    
def default_key():
    return random_hex(20)


def send_with_send_mail(subject , message , to_email):
    from_email = 'ta664054@gmail.com'
    send_mail(from_email=from_email,subject=subject, message=message,recipient_list=to_email)

class VerificationOTP(models.Model):
    unverified_email = models.EmailField(max_length = 80, unique=True) #R
    secret_key = models.CharField(
        max_length=40,
        default=default_key,
        validators=[hex_validator],
        help_text="Hex-encoded secret key to generate totp tokens.",
        unique=True,
    )
    last_verified_counter = models.BigIntegerField(
        default=-1,
        help_text=("The counter value of the latest verified token."
                   "The next token must be at a higher counter value."
                   "It makes sure a token is used only once.")
    )
    verified = models.BooleanField(default=False)

    step = 300
    digits = 6
    
    def totp_obj(self):
        totp = TOTP(key=self.secret_key.encode('utf-8'), step=self.step, digits=self.digits)
        totp.time = time.time()
        return totp

    def generate_challenge(self):
        totp = self.totp_obj()
        token = str(totp.token()).zfill(self.digits)

        message ="Your token for Verification is {token_value} It is valid for {time_validity} minutes."
        message = message.format(
            token_value=token, time_validity=self.step // 60)
        print('test token: ', self.unverified_email)
        send_with_send_mail(subject="VerificationOTP", message=message,to_email=[self.unverified_email])
        print('Dooooone')
        print('token: ', token)
        return token

    

    def verify_token(self, token, tolerance=1):
        try:
            token = int(token)
        except ValueError:
            self.verified = False
        totp = self.totp_obj()

        if ((totp.t() > self.last_verified_counter) and (totp.verify(token, tolerance=0))):
            self.last_verified_counter = totp.t()
            self.verified = True
            self.save()
        else:
            self.verified = False
        return self.verified
    
