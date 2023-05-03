from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Work(models.Model):
    YOUTUBE = 'YT'
    INSTAGRAM = 'IG'
    OTHER = 'OT'
    WORK_TYPE_CHOICES = [
        (YOUTUBE, 'Youtube'),
        (INSTAGRAM, 'Instagram'),
        (OTHER, 'Other')
    ]
    link = models.URLField(max_length=200)
    work_type = models.CharField(max_length=2, choices=WORK_TYPE_CHOICES)

    def __str__(self):
        return self.link

class Artist(models.Model):
    name = models.CharField(max_length=100)
    works = models.ManyToManyField(Work)

    def __str__(self):
        return self.name