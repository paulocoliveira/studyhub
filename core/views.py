from django.shortcuts import redirect
from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().get(request, *args, **kwargs)
