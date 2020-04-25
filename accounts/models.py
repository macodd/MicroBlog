import os
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models.signals import post_save


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = instance.user.username
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'images/{new_filename}/{final_filename}'


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    @staticmethod
    def is_following(user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    image       = models.ImageField(default='images/default_avatar.jpg', upload_to=upload_image_path, blank=True, null=True)
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def get_following(self):
        return self.following.all().exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy('profiles:follow', kwargs={'username': self.user.username})

    def get_absolute_url(self):
        return reverse_lazy('profiles:detail', kwargs={'username': self.user.username})


def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        # celery + redis


post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
