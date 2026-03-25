from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CategoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'categories/list.html'
