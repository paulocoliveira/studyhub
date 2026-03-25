from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class InsightsIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'insights/index.html'
