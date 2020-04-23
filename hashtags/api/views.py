from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from tweets.api.pagination import StandardResultsPagination
from tweets.api.serializers import TweetModelSerializer

from hashtags.models import HashTag


class HashTagAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hashtag = self.kwargs.get('hashtag')
        hashtag_obj, created = HashTag.objects.get_or_create(tag=hashtag)
        qs = hashtag_obj.get_tweets()
        return qs
