from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .pagination import StandardResultsPagination
from .serializers import TweetModelSerializer
from tweets.models import Tweet


class RetweetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tweet_qs = Tweet.objects.filter(pk=pk)
        if tweet_qs.exists() and tweet_qs.count() == 1:
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
            if new_tweet is not None:
                data = TweetModelSerializer(new_tweet).data
                return Response(data)
        return Response({'message': 'Not Allowed'}, status=400)


class TweetCreateAPIView(CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        requested_user = self.kwargs.get("username")
        if requested_user:
            qs = Tweet.objects.filter(user__username=requested_user).order_by('-timestamp')
        else:
            i_follow = self.request.user.profile.get_following()
            qs1 = Tweet.objects.filter(user__in=i_follow).order_by('-timestamp')
            qs2 = Tweet.objects.filter(user=self.request.user)
            qs = (qs1 | qs2).distinct().order_by('-timestamp')
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs
