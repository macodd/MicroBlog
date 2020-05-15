"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from tweets.views import TweetListView
from tweets.api.views import SearchAPIView

from hashtags.views import HashTagView
from hashtags.api.views import HashTagAPIView

from .views import (
    UserLoginView,
    UserLogoutView,
    SearchView,
    TermsView,
    ContactFormView,
)


urlpatterns = [
    path('', TweetListView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('tweet/', include('tweets.urls', namespace='tweet')),
    path('register/', include('register.urls', namespace='register')),
    path('search/', SearchView.as_view(), name='search'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('profiles/', include('accounts.urls', namespace='profiles')),
    path('api/tweet/', include('tweets.api.urls', namespace='tweet-api')),
    path('api/search/',SearchAPIView.as_view(), name='search-api'),
    path('api/tag/<str:hashtag>/',HashTagAPIView.as_view(), name='tag-api'),
    path('api/profiles/', include('accounts.api.urls', namespace='profile-api')),
    path('tags/<str:hashtag>/', HashTagView.as_view(), name='hashtag'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
