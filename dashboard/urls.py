from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import path
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'


app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
