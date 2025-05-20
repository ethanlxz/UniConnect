from rest_framework import serializers
from .models import Class

class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name', 'max_students']
        read_only_fields = ['code']