from rest_framework import serializers
from .models import User

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
        print('Updating')
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
    


    