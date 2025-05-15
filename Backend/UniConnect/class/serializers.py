from rest_framework import serializers
from .models import Class

class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name']
        read_only_fields = ['code']