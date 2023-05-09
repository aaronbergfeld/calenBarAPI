from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Task(models.Model):
    title = models.CharField(max_length=200)
    priority = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    color = models.CharField(max_length=100)
    description = models.TextField()
    estimated_time = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    color_theme = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.title
