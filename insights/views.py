import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from categories.models import Category
from dashboard.services import DashboardService

from .services import AIService, check_rate_limit


def _render_markdown(text):
    """Convert basic markdown to HTML for safe display. Escapes HTML first."""
    import html
    text = html.escape(text)
    # bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # numbered list items — wrap consecutive <li> blocks in <ol>
    text = re.sub(r'(?m)^(\d+)\. (.+)$', r'<li>\2</li>', text)
    text = re.sub(r'((?:<li>[^<]*</li>\n?)+)', r'<ol class="list-decimal list-inside space-y-1">\1</ol>', text)
    # bullet list items — use placeholder tag to avoid collision, then wrap in <ul>
    text = re.sub(r'(?m)^[-•] (.+)$', r'<blt>\1</blt>', text)
    text = re.sub(
        r'((?:<blt>[^<]*</blt>\n?)+)',
        lambda m: '<ul class="list-disc list-inside space-y-1">'
            + m.group(1).replace('<blt>', '<li>').replace('</blt>', '</li>')
            + '</ul>',
        text,
    )
    text = re.sub(r'<blt>(.*?)</blt>', r'<li>\1</li>', text)
    # newlines to br (after list processing)
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = text.replace('\n', '<br>')
    return f'<p>{text}</p>'


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
            Category.objects.all().values_list('name', flat=True)
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

        result = AIService(user=request.user).suggest_category(title, url or None, category_names)

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

        result = AIService(user=request.user).generate_description(
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
        result = AIService(user=request.user).generate_insights(stats)

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


class SuggestNextView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not check_rate_limit(request.session, 'suggest_next', max_calls=5):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )
        result = AIService(user=request.user).suggest_next(request.user)
        if result is None:
            return JsonResponse(
                {'success': False, 'error': 'AI service unavailable or no content to analyze.'},
                status=503,
            )
        return JsonResponse({'success': True, 'html': _render_markdown(result)})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class ForgottenContentsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from django.utils import timezone
        now_ts = timezone.now()
        items = DashboardService(user=request.user).get_forgotten_contents(days=30)
        data = []
        for item in items:
            days_since = (now_ts - item.created_at).days
            data.append({
                'id': item.pk,
                'title': item.title,
                'content_type': item.content_type,
                'days_since_saved': days_since,
                'detail_url': f'/contents/{item.pk}/',
            })
        return JsonResponse({'success': True, 'items': data})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class AnalyzeTopicsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not check_rate_limit(request.session, 'analyze_topics', max_calls=5):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )
        result = AIService(user=request.user).analyze_topics(request.user)
        if result is None:
            return JsonResponse(
                {'success': False, 'error': 'Not enough data to analyze topics yet.'},
                status=503,
            )
        return JsonResponse({'success': True, 'html': _render_markdown(result)})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class WeeklySummaryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not check_rate_limit(request.session, 'weekly_summary', max_calls=5):
            return JsonResponse(
                {'success': False, 'error': 'Rate limit exceeded. Please try again later.'},
                status=429,
            )
        result = AIService(user=request.user).weekly_summary(request.user)
        if result is None:
            return JsonResponse(
                {'success': False, 'error': 'AI service unavailable. Please try again later.'},
                status=503,
            )
        return JsonResponse({'success': True, 'html': _render_markdown(result)})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class ChatView(LoginRequiredMixin, View):
    DAILY_CHAT_LIMIT = 20

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        message = (data.get('message') or '').strip()
        history = data.get('history', [])

        if not message:
            return JsonResponse({'success': False, 'error': 'Message is required'}, status=400)

        # validate history structure
        if not isinstance(history, list):
            history = []
        history = [
            h for h in history
            if isinstance(h, dict) and h.get('role') in ('user', 'assistant') and h.get('content')
        ]

        if not check_rate_limit(request.session, 'chat', max_calls=self.DAILY_CHAT_LIMIT, window_seconds=86400):
            return JsonResponse(
                {'success': False, 'error': 'Daily chat limit reached. Come back tomorrow!'},
                status=429,
            )

        reply = AIService(user=request.user).chat(request.user, message, history)

        if reply is None:
            return JsonResponse(
                {'success': False, 'error': 'AI service unavailable. Please try again.'},
                status=503,
            )

        return JsonResponse({'success': True, 'reply': reply})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
