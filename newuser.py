from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)