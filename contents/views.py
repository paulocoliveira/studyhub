from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ContentListView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/list.html'
