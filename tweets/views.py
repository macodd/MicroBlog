# from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Tweet


class TweetDetailView(DetailView):
    template_name = 'tweets/detail_view.html'
    model = Tweet


class TweetListView(ListView):
    template_name = 'tweets/list_view.html'
    model = Tweet
    paginate_by = 10


# def tweet_detail_view(request, id=1):
#     obj = Tweet.objects.get(id=id)
#     context = {
#         'tweet': obj
#     }
#     return render(request, 'tweets/detail_view.html', context)
#
#
# def tweet_list_view(request):
#     query = Tweet.objects.all()
#     context = {
#         'tweet_list': query
#     }
#     return render(request, 'tweets/list_view.html', context)
