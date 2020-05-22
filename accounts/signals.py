from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .tasks import register_confirmation_mail
from .models import UserProfile


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()
        register_confirmation_mail.delay(instance.first_name, instance.email)
