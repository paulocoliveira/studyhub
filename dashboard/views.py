from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services import DashboardService


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = DashboardService(user=self.request.user)
        context['stats'] = service.get_stats()
        context['recent_added'] = service.get_recent_added()
        context['recent_completed'] = service.get_recent_completed()
        context['top_categories'] = service.get_top_categories()
        context['top_tags'] = service.get_top_tags()
        return context
