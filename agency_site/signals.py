
#  Trained with signals but dont use them in project now

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Clients

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_handler(sender, instance, created, **kwargs):
    """
    Once a new User instance was saved:
    Check User instance, if this is new instance (created is True)
    then create a Profile for this user.
    """
    if not created:
        return
    default_data = dict(full_name='', email='', username='', password='', tel_number='')
    instance.profile = Clients.objects.create(user=instance, **default_data)


