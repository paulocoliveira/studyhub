from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class TagListView(LoginRequiredMixin, TemplateView):
    template_name = 'tags/list.html'
