import re
from django.db.models.signals import post_save
from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.timezone import now

from hashtags.signals import parsed_hashtags

from accounts.models import UserProfile


class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        qs = self.get_queryset().filter(
            user=user, parent=og_parent
            ).filter(
                timestamp__year=now().year,
                timestamp__month=now().month,
                timestamp__day=now().day
            )

        if qs.exists():
            return None

        obj = self.model(
            parent=og_parent,
            user=user,
            content=og_parent.content
        )
        obj.save()
        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked


class Tweet(models.Model):
    parent      = models.ForeignKey('self',
                                    blank=True,
                                    null=True,
                                    on_delete=models.CASCADE
                                    )
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    )
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         blank=True,
                                         related_name='liked')
    content     = models.CharField(max_length=140)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse_lazy('tweet:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp']


def tweet_save_receiver(sender, instance, created, **kwargs):
    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)
        # notifications app

        hashtag_regex = r'#(?P<hashtag>[\w\d+-]+)'
        hashtags = re.findall(hashtag_regex, instance.content)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)


post_save.connect(tweet_save_receiver, sender=Tweet)
