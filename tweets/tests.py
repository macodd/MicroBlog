from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Tweet

User = get_user_model()


class TweeTModelTestCase(TestCase):
    def setUp(self) -> None:
        bot = User.objects.create(username='test_bot')

    def test_tweet_item(self):
        obj = Tweet.objects.create(
            user=User.objects.first(),
            content='Content being tested'
        )
        self.assertTrue(obj.content == 'Content being tested')
        self.assertTrue(obj.id == 1)
