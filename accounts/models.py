from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

from .utils import upload_image_path


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def random(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs.order_by("?")

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile = UserProfile.objects.get(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile = UserProfile.objects.get(user=user)
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    image           = models.ImageField(upload_to=upload_image_path,
                                    blank=True,
                                    null=True)
    following       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def get_following(self):
        return self.following.all().exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy('profiles:follow', kwargs={'username': self.user.username})

    def get_absolute_url(self):
        return reverse_lazy('profiles:detail', kwargs={'username': self.user.username})

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         rotate_image(self)
    #     return super().save(*args, **kwargs)
