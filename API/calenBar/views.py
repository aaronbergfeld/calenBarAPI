from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    
    @action(detail=True, methods=['post'])
    def add_task(self, request, pk=None):
        calendar = self.get_object()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            calendar.tasks.add(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_task(self, request, pk=None):
        calendar = self.get_object()
        task = Task.objects.get(id=request.data['id'])
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def delete_task(self, request, pk=None):
        calendar = self.get_object()
        task = Task.objects.get(id=request.data['id'])
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

