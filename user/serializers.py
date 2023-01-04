from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        is_staff = validated_data.get('is_superuser')
        if is_staff:
            user = User.objects.create_staff(password=password , **validated_data)

        else:
            user = User.objects.create_user(password=password,**validated_data)
            
        user.save()
        return user
    
    def update(self, instance ,validated_data):
        password = validated_data.pop('password', '')
        firstname = validated_data.pop('firstname', '')
        lastname = validated_data.pop('lastname', '')
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        if password:
            instance.set_password(password)
        
        if firstname:
            print('First name changed')
            instance.firstname = firstname
            
        if lastname:
            instance.lastname = lastname
            
        instance.save()
        return instance
    
    
class OtpEmail(serializers.ModelSerializer):
    class Meta:
        model = VerificationOTP
        fields = '__all__'
        
    def create(self, validated_data):
        unverified_email = validated_data.get('unverified_email')
        print(unverified_email)
        otp_verification = VerificationOTP.objects.create(unverified_email=unverified_email)
        print(otp_verification.id)
        token = otp_verification.generate_challenge()
        return otp_verification

class Verify_token(serializers.ModelSerializer):
    unverified_email = serializers.EmailField()
    token = serializers.CharField()
    class Meta:
        model = VerificationOTP
        fields = '__all__'