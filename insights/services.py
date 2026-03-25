import time

import anthropic
import openai as openai_sdk
from django.conf import settings


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

    def generate_insights(self, user_stats):
        """
        Returns a markdown analysis string of the user's learning habits, or None on failure.
        """
        total = user_stats.get('total_contents', 0)
        by_status = user_stats.get('by_status', {})
        by_type = user_stats.get('by_type', [])
        prompt = (
            f'Analyze these learning content statistics and give 3-5 bullet points of insights '
            f'and 2-3 actionable suggestions. Be encouraging and concise. '
            f'Format with **bold** headers.\n\n'
            f'Total items: {total}\n'
            f'By status: {by_status}\n'
            f'By type: {by_type}'
        )
        return self._call_ai(prompt)
