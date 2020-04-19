from rest_framework.generics import ListAPIView
from django.db.models import Q

from .serializers import TweetModelSerializer
from tweets.models import Tweet


class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        qs = Tweet.objects.all()
        query = self.request.GET.get('q', None)
        print(query)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs
