import time

import anthropic
import openai as openai_sdk
from django.conf import settings


def build_user_context(user):
    """
    Build a full snapshot of the user's learning library for use as RAG context.
    Includes every saved content item with all relevant fields.
    """
    from django.db.models import Count
    from contents.models import Content
    from categories.models import Category
    from tags.models import Tag

    total = Content.objects.filter(user=user).count()
    completed = Content.objects.filter(user=user, status='completed').count()
    in_progress = Content.objects.filter(user=user, status='in_progress').count()
    new_count = Content.objects.filter(user=user, status='new').count()
    completion_rate = round((completed / total * 100) if total > 0 else 0, 1)

    all_contents = (
        Content.objects.filter(user=user)
        .select_related('category')
        .prefetch_related('tags')
        .order_by('category__name', 'title')
    )

    lines = [
        '=== USER LIBRARY SNAPSHOT ===',
        f'Total items: {total} | Completed: {completed} ({completion_rate}%) '
        f'| In progress: {in_progress} | New: {new_count}',
        '',
        '=== FULL CONTENT LIST ===',
    ]

    for item in all_contents:
        cat = item.category.name if item.category else 'Uncategorized'
        tags = ', '.join(item.tags.values_list('name', flat=True)) or 'none'
        desc = (item.description or '').strip()
        desc_snippet = (desc[:120] + '…') if len(desc) > 120 else desc
        url_line = f' | url: {item.url}' if item.url else ''
        desc_line = f'\n    description: {desc_snippet}' if desc_snippet else ''
        lines.append(
            f'[{item.pk}] "{item.title}"'
            f' | type: {item.content_type}'
            f' | status: {item.status}'
            f' | category: {cat}'
            f' | tags: {tags}'
            f'{url_line}'
            f'{desc_line}'
        )

    return '\n'.join(lines)


def check_rate_limit(session, action_key, max_calls=10, window_seconds=3600):
    """
    Check if an AI action is within its rate limit for the current session.

    Returns True if the call is allowed, False if the limit is exceeded.
    """
    count_key = f'ai_rate_{action_key}_count'
    window_key = f'ai_rate_{action_key}_window'

    now = time.time()
    window_start = session.get(window_key)
    call_count = session.get(count_key, 0)

    if window_start is None or (now - window_start) >= window_seconds:
        session[window_key] = now
        session[count_key] = 1
        return True

    if call_count >= max_calls:
        return False

    session[count_key] = call_count + 1
    return True


class AIService:
    ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001'
    OPENAI_MODEL = 'gpt-4o-mini'

    def __init__(self, user=None):
        self.user = user
        self.provider = getattr(user, 'ai_provider', 'anthropic') if user else 'anthropic'
        api_key = (getattr(user, 'ai_api_key', '') or '') if user else ''
        if not api_key:
            api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
        self.api_key = api_key

    def _call_ai(self, prompt: str) -> str | None:
        """Send a prompt to the configured AI provider. Returns text or None on failure."""
        if not self.api_key:
            return None
        try:
            if self.provider == 'openai':
                client = openai_sdk.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.OPENAI_MODEL,
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=500,
                )
                return response.choices[0].message.content.strip()
            else:
                client = anthropic.Anthropic(api_key=self.api_key)
                response = client.messages.create(
                    model=self.ANTHROPIC_MODEL,
                    max_tokens=500,
                    messages=[{'role': 'user', 'content': prompt}],
                )
                return response.content[0].text.strip()
        except Exception:
            return None

    def suggest_category(self, title, url, user_categories):
        """
        Returns the best matching category name string from user_categories, or None on failure.
        """
        if not user_categories:
            return None
        cats = ', '.join(user_categories)
        prompt = (
            f'Given a content item titled "{title}"'
            + (f' with URL {url}' if url else '')
            + f', and these available categories: {cats}. '
            f'Reply with ONLY the single best matching category name from the list, nothing else.'
        )
        result = self._call_ai(prompt)
        if not result:
            return None
        result_lower = result.strip().lower()
        for cat in user_categories:
            if cat.lower() == result_lower:
                return cat
        return user_categories[0]

    def generate_description(self, title, url, content_type):
        """
        Returns a concise 2-3 sentence description string, or None on failure.
        """
        prompt = (
            f'Write a concise 2-3 sentence description for a {content_type or "content"} '
            f'titled "{title}"'
            + (f' at {url}' if url else '')
            + '. Return only the description, no labels or preamble.'
        )
        return self._call_ai(prompt)

    def _call_ai_messages(self, messages, system_prompt=None, max_tokens=800):
        if not self.api_key:
            return None
        try:
            if self.provider == 'openai':
                msgs = []
                if system_prompt:
                    msgs.append({'role': 'system', 'content': system_prompt})
                msgs.extend(messages)
                client = openai_sdk.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.OPENAI_MODEL,
                    messages=msgs,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content.strip()
            else:
                client = anthropic.Anthropic(api_key=self.api_key)
                response = client.messages.create(
                    model=self.ANTHROPIC_MODEL,
                    max_tokens=max_tokens,
                    system=system_prompt or '',
                    messages=messages,
                )
                return response.content[0].text.strip()
        except Exception:
            return None

    def suggest_next(self, user):
        from django.utils import timezone
        from datetime import timedelta
        from contents.models import Content
        now = timezone.now()
        items = (
            Content.objects
            .filter(user=user, status__in=['new', 'in_progress'])
            .select_related('category')
            .prefetch_related('tags')
            .order_by('created_at')[:20]
        )
        if not items:
            return None
        lines = []
        for item in items:
            days = (now - item.created_at).days
            tags = ', '.join(item.tags.values_list('name', flat=True)) or 'none'
            cat = item.category.name if item.category else 'uncategorized'
            lines.append(
                f'- "{item.title}" | type: {item.content_type} | status: {item.status}'
                f' | category: {cat} | tags: {tags} | saved {days} days ago'
            )
        content_list = '\n'.join(lines)
        prompt = (
            f'You are a learning coach. Based on this list of content items the user has saved but not finished, '
            f'recommend 3-5 items they should study next. For each, give a one-line reason.\n\n'
            f'Content list:\n{content_list}\n\n'
            f'Format your response as a numbered list. Be concise and encouraging.'
        )
        return self._call_ai(prompt)

    def analyze_topics(self, user):
        from django.db.models import Count
        from categories.models import Category
        from tags.models import Tag
        top_categories = (
            Category.objects
            .filter(user=user)
            .annotate(count=Count('contents'))
            .filter(count__gt=0)
            .order_by('-count')[:5]
        )
        top_tags = (
            Tag.objects
            .filter(user=user)
            .annotate(count=Count('contents'))
            .filter(count__gt=0)
            .order_by('-count')[:10]
        )
        if not top_categories and not top_tags:
            return None
        cat_lines = '\n'.join(f'- {c.name}: {c.count} items' for c in top_categories) or 'No categories yet.'
        tag_lines = '\n'.join(f'- {t.name}: {t.count} items' for t in top_tags) or 'No tags yet.'
        prompt = (
            f'You are a learning strategist. Based on these learning topics, identify patterns '
            f'and suggest 2-3 specific directions for deeper study. Be actionable and encouraging.\n\n'
            f'Top categories:\n{cat_lines}\n\n'
            f'Top tags:\n{tag_lines}\n\n'
            f'Format: brief pattern observation, then numbered list of suggestions.'
        )
        return self._call_ai(prompt)

    def weekly_summary(self, user):
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count
        from contents.models import Content
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        completed_this_week = Content.objects.filter(
            user=user, status='completed', updated_at__gte=week_ago
        ).count()
        added_this_week = Content.objects.filter(
            user=user, created_at__gte=week_ago
        ).count()
        in_progress = Content.objects.filter(user=user, status='in_progress').count()
        active_cat = (
            Content.objects
            .filter(user=user, updated_at__gte=week_ago, category__isnull=False)
            .values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        active_area = active_cat['category__name'] if active_cat else 'general topics'
        prompt = (
            f'Write a brief, encouraging 2-3 sentence weekly learning summary for someone who:\n'
            f'- Completed {completed_this_week} item(s) this week\n'
            f'- Added {added_this_week} new item(s) this week\n'
            f'- Has {in_progress} item(s) currently in progress\n'
            f'- Was most active in: {active_area}\n\n'
            f'Be warm, specific, and motivational. Return only the summary text.'
        )
        return self._call_ai(prompt)

    def chat(self, user, message, history):
        """
        Multi-turn chat grounded exclusively in the user's saved library data (RAG-style).
        history: list of {'role': 'user'|'assistant', 'content': str}
        Returns assistant reply string or None on failure.
        """
        context = build_user_context(user)
        system_prompt = (
            'You are a personal study assistant for StudyHub. '
            'Your job is to help the user navigate and reflect on their own saved learning library.\n\n'
            'STRICT RULES — follow these without exception:\n'
            '1. Answer ONLY based on the data provided below. Do not use any external knowledge, '
            'do not reference anything outside this dataset, and do not search the internet.\n'
            '2. If the user asks about something not present in their library, say clearly: '
            '"I don\'t see that in your library." Do not guess, infer, or fill gaps with general knowledge.\n'
            '3. Do not recommend content, authors, books, courses, or resources that are not explicitly '
            'listed in the data below.\n'
            '4. Do not make up titles, descriptions, categories, or any other field values.\n'
            '5. You may reason about patterns, counts, and relationships within the provided data '
            '(e.g. "you have 3 items in the QA category", "you haven\'t finished X yet").\n'
            '6. Be concise and direct. Avoid filler phrases.\n\n'
            f'{context}'
        )
        messages = list(history) + [{'role': 'user', 'content': message}]
        return self._call_ai_messages(messages, system_prompt=system_prompt, max_tokens=600)

    def generate_insights(self, user_stats):
        """
        Returns an HTML analysis string of the user's learning habits, or None on failure.
        """
        total = user_stats.get('total_contents', 0)
        by_status = user_stats.get('by_status', {})
        by_type = user_stats.get('by_type', [])
        prompt = (
            f'Analyze these learning content statistics and give 3-5 bullet points of insights '
            f'and 2-3 actionable suggestions. Be encouraging and concise. '
            f'Format your response using HTML tags: use <ul> and <li> for bullet points, '
            f'<strong> for emphasis, and <p> for paragraphs.\n\n'
            f'Total items: {total}\n'
            f'By status: {by_status}\n'
            f'By type: {by_type}'
        )
        return self._call_ai(prompt)
