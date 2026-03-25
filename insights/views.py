import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from categories.models import Category
from dashboard.services import DashboardService

from .services import AIService, check_rate_limit


class InsightsIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'insights/index.html'


class SuggestCategoryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        title = data.get('title', '').strip()
        url = data.get('url', '').strip()

        if not title:
            return JsonResponse(
                {'success': False, 'error': 'Title is required'}, status=400
            )

        category_names = list(
            Category.objects.filter(user=request.user).values_list('name', flat=True)
        )

        if not category_names:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'Create at least one category before using AI suggestions.',
                },
                status=400,
            )

        if not check_rate_limit(request.session, 'suggest_category'):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )

        result = AIService().suggest_category(title, url or None, category_names)

        if result is None:
            return JsonResponse(
                {'success': False, 'error': 'AI service unavailable'}, status=503
            )

        return JsonResponse({'success': True, 'category': result})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class GenerateDescriptionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        title = data.get('title', '').strip()
        url = data.get('url', '').strip()
        content_type = data.get('content_type', '').strip()

        if not title:
            return JsonResponse(
                {'success': False, 'error': 'Title is required'}, status=400
            )

        if not check_rate_limit(request.session, 'generate_description'):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )

        result = AIService().generate_description(
            title, url or None, content_type or None
        )

        if result is None:
            return JsonResponse(
                {'success': False, 'error': 'AI service unavailable'}, status=503
            )

        return JsonResponse({'success': True, 'description': result})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class GenerateInsightsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not check_rate_limit(request.session, 'generate_insights', max_calls=5):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )

        stats = DashboardService(user=request.user).get_stats()
        result = AIService().generate_insights(stats)

        if result is None:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'AI service unavailable. Please try again later.',
                },
                status=503,
            )

        return JsonResponse({'success': True, 'insights': result})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
