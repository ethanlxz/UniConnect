from rest_framework import serializers
from .models import StudentProfile, LecturerProfile
from django.contrib.auth.hashers import make_password

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'name', 'password', 'contact_num', 'gender', 'major', 'profile_image', 'bio', 'instagram_id']
        extra_kwargs = {'password': {'write_only': True},
                        'profile_image': {'required': False},
                        'bio': {'required': False},
                        'instagram_id': {'required': False}}
        
    def validate_instagram_id(self, value):
        if value and not value.startswith('@'):
            raise serializers.ValidationError("Instagram ID must start with '@'.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    
class LecturerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = ['id', 'username', 'email', 'name', 'password', 'contact_num', 'major', 'profile_image']
        extra_kwargs = {'password': {'write_only': True},
                        'profile_image': {'required': False}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)