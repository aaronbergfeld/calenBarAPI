from django.db import models

# Create your models here.

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
    title = models.CharField(max_length=200)
    description = models.TextField()
    color_theme = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.title
