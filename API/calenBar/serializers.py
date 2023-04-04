from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'start_date', 'end_date', 'color', 'description', 'estimated_time', 'completed']
        
class CalendarSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Calendar
        fields = ['id', 'title', 'description', 'color_theme', 'tasks']