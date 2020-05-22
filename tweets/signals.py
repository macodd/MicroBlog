from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import re

from hashtags.signals import parsed_hashtags
from .tasks import mentioned_tweet_mail
from .models import Tweet


@receiver(post_save, sender=Tweet)
def tweet_save_receiver(sender, instance, created, **kwargs):
    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)
        for u in usernames:
            qs = User.objects.filter(username__iexact=u)
            if qs.exists():
                user_obj = qs.first()
                mentioned_tweet_mail.delay(user_obj.email, instance.pk)

        hashtag_regex = r'#(?P<hashtag>[\w\d+-]+)'
        hashtags = re.findall(hashtag_regex, instance.content)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
