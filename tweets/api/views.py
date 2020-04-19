from rest_framework.generics import ListAPIView

from .serializers import TweetModelSerializer
from tweets.models import Tweet


class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        return Tweet.objects.all()
