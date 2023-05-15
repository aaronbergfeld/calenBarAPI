from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
        serializer = TaskSerializer(data=request.data)
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

    def get_queryset(self):
        user = self.request.user
        return Calendar.objects.filter(user=user)

    def create(self, request):
        user = self.request.user
        request.data['user'] = user.id
        request.data['tasks'] = []
        print(request.data)
        calendar_serializer = CalendarSerializer(data=request.data)
        if calendar_serializer.is_valid():
            calendar_serializer.save()
            return Response(calendar_serializer.data, status=status.HTTP_201_CREATED)
        return Response(calendar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def logout(self, request, pk=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calendar = Calendar(user=user, title=user.username + "'s Calendar")
            calendar.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

