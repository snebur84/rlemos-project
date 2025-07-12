# projetos/serializers.py
from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='manager', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'manager', 'manager_id']
        read_only_fields = ['created_at', 'updated_at']