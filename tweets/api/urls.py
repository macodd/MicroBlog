from django.urls import path

from .views import(TweetListAPIView,
                   TweetCreateAPIView,
                   RetweetAPIView,
                   LikeTweetAPIView,
                   TweetDetailView
                   )

app_name = 'tweets'


urlpatterns = [
    path('', TweetListAPIView.as_view(), name='list'),  # /api/tweet/
    path('create/', TweetCreateAPIView.as_view(), name='create'),  # /api/tweet/create/
    path('<int:pk>/', TweetDetailView.as_view(), name='detail'),  # /api/tweet/pk/tweet
    path('<int:pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),  # /api/tweet/pk/tweet
    path('<int:pk>/liked/', LikeTweetAPIView.as_view(), name='liked'),  # /api/tweet/pk/tweet
]
