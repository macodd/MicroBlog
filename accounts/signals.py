from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile

from .tasks import register_confirmation_mail


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        register_confirmation_mail.delay(instance.first_name, instance.email)


@receiver(post_save, sender=User)
def save_user_receiver(sender, instance, created, **kwargs):
    instance.profile.save()