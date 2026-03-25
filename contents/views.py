from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ContentFilterForm, ContentForm
from .models import STATUS_CHOICES, Content
from .services import LinkPreviewService

ALLOWED_SORT_FIELDS = ['title', '-title', 'status', 'created_at', '-created_at']


class ContentListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'contents/content_list.html'
    context_object_name = 'contents'
    paginate_by = 12

    def get_queryset(self):
        qs = Content.objects.filter(user=self.request.user)

        q = self.request.GET.get('search', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        status = self.request.GET.get('status', '').strip()
        if status:
            qs = qs.filter(status=status)

        content_type = self.request.GET.get('content_type', '').strip()
        if content_type:
            qs = qs.filter(content_type=content_type)

        category = self.request.GET.get('category', '').strip()
        if category:
            qs = qs.filter(category__id=category)

        tag = self.request.GET.get('tag', '').strip()
        if tag:
            qs = qs.filter(tags__id=tag)

        sort = self.request.GET.get('sort', '-created_at').strip()
        if sort not in ALLOWED_SORT_FIELDS:
            sort = '-created_at'
        qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ContentFilterForm(
            self.request.GET or None,
            user=self.request.user,
        )
        return context


class ContentDetailView(LoginRequiredMixin, DetailView):
    model = Content
    template_name = 'contents/content_detail.html'
    context_object_name = 'content'

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user)


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'contents/content_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Content created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contents:list')


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'contents/content_form.html'

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Content updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contents:detail', kwargs={'pk': self.object.pk})


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'contents/content_confirm_delete.html'
    success_url = reverse_lazy('contents:list')

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Content deleted successfully.')
        return super().form_valid(form)


class ContentStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = get_object_or_404(Content, pk=pk, user=request.user)
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in STATUS_CHOICES]
        if new_status in valid_statuses:
            content.status = new_status
            content.save(update_fields=['status', 'updated_at'])
            messages.success(
                request,
                f'Status updated to {content.get_status_display()}.',
            )
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer or reverse('contents:list'))


class RefreshPreviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = get_object_or_404(Content, pk=pk, user=request.user)
        if not content.url:
            return JsonResponse(
                {'success': False, 'error': 'No URL set for this content.'},
                status=400,
            )
        preview = LinkPreviewService().fetch_preview(content.url)
        if preview and preview.get('preview_image_url'):
            content.preview_image_url = preview['preview_image_url']
            content.save(update_fields=['preview_image_url'])
            return JsonResponse(
                {'success': True, 'preview_image_url': content.preview_image_url}
            )
        return JsonResponse(
            {'success': False, 'error': 'No preview image found for this URL.'},
            status=404,
        )
