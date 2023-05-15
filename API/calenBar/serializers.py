from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'start_date', 'end_date', 'goal_end_date', 'color', 'description', 'estimated_time', 'is_event', 'event_duration', 'completed']
        
class CalendarSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Calendar
        fields = ['id', 'user', 'title', 'description', 'tasks']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
