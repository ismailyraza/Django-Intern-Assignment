First, we define the models in a models.py file:

from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    works = models.ManyToManyField('Work')

    def __str__(self):
        return self.name


class Work(models.Model):
    LINK_TYPES = (
        ('Youtube', 'Youtube'),
        ('Instagram', 'Instagram'),
        ('Other', 'Other'),
    )

    link = models.URLField()
    work_type = models.CharField(max_length=50, choices=LINK_TYPES)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.link

Next, we define a signal to create a Client object after a new User object is created:

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, User


@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance, name=instance.username)

Finally, we define the REST API views in a views.py file:

from rest_framework import generics, filters
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from .models import Client, Artist, Work
from .serializers import ClientSerializer, ArtistSerializer, WorkSerializer, UserSerializer


class WorkList(generics.ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['work_type']
    search_fields = ['artist__name']


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ClientDetail(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ArtistDetail(generics.RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer