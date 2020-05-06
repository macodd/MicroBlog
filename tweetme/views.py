from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView
from django.shortcuts import render

User = get_user_model()


class ThanksForRegistering(TemplateView):
    template_name = 'thanks.html'


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        qs = None
        if query:
            qs = User.objects.filter(
                username__icontains=query
            )
        context = {'users': qs}
        return render(request, 'search_view.html', context)
