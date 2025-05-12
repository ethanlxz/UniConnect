from rest_framework import serializers
from .models import StudentProfile, LecturerProfile
from django.contrib.auth.hashers import make_password

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'name', 'password', 'age', 'contact_num']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class LecturerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = ['id', 'username', 'email', 'name', 'password', 'contact_num']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)