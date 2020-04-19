from django.db import models
from django.urls import reverse_lazy
from django.conf import settings


class Tweet(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content     = models.CharField(max_length=140)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse_lazy('tweet:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp']
