from rest_framework import serializers
from .models import Class

class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name', 'max_students', 'group', 'min_group_members']
        read_only_fields = ['code']

    # Validate that min_group_members does not exceed max_students
    def validate(self, data):
        if data.get('min_group_members', 1) > data.get('max_students', 0):
            raise serializers.ValidationError("Minimum group members cannot exceed max students.")
        return data