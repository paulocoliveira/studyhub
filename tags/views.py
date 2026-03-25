from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import TagForm
from .models import Tag


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tags/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return (
            Tag.objects.filter(user=self.request.user)
            .annotate(content_count=Count('contents'))
        )


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Tag created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tags:list')


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tags:list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tag deleted successfully.')
        return super().form_valid(form)
