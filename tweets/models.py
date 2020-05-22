from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.conf import settings
from django.db import models


from accounts.models import UserProfile

User = get_user_model()


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
    content     = models.CharField(max_length=320)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects = TweetManager()

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('tweet:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp']
