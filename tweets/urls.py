from django.urls import path

# from .views import tweet_detail_view, tweet_list_view
from .views import TweetDetailView, TweetListView, TweetCreateView
app_name = 'tweets'

urlpatterns = [
    path('', TweetListView.as_view(), name='list'),
    path('create/', TweetCreateView.as_view(), name='create'),
    path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
]