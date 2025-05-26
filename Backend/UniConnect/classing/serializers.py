from rest_framework import serializers
from .models import Class

class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name', 'max_students', 'group', 'max_group_members']
        read_only_fields = ['code']