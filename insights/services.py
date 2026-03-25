import time

import anthropic
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
    MODEL = 'claude-haiku-4-5-20251001'

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def suggest_category(self, title, url, user_categories):
        """
        Returns the best matching category name string from user_categories, or None on failure.
        """
        if not user_categories:
            return None

        categories_list = ', '.join(user_categories)
        url_part = f' (URL: {url})' if url else ''
        prompt = (
            f'Given this content:\n'
            f'Title: {title}{url_part}\n\n'
            f'And these available categories: {categories_list}\n\n'
            f'Which single category best matches this content? '
            f'Reply with ONLY the category name, nothing else.'
        )

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=100,
                messages=[{'role': 'user', 'content': prompt}],
            )
            result_text = response.content[0].text.strip()
            for category in user_categories:
                if category.lower() == result_text.lower():
                    return category
            return user_categories[0]
        except anthropic.APIError:
            return None
        except anthropic.APIConnectionError:
            return None
        except anthropic.RateLimitError:
            return None
        except anthropic.APITimeoutError:
            return None
        except Exception:
            return None

    def generate_description(self, title, url, content_type):
        """
        Returns a concise 2-3 sentence description string, or None on failure.
        """
        url_part = f' (URL: {url})' if url else ''
        type_part = f' (type: {content_type})' if content_type else ''
        prompt = (
            f'Given this content:\n'
            f'Title: {title}{url_part}{type_part}\n\n'
            f'Write a concise 2-3 sentence description of what this content is likely about, '
            f'suitable for a personal knowledge base. '
            f'Reply with ONLY the description text, nothing else.'
        )

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=200,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return response.content[0].text.strip()
        except anthropic.APIError:
            return None
        except anthropic.APIConnectionError:
            return None
        except anthropic.RateLimitError:
            return None
        except anthropic.APITimeoutError:
            return None
        except Exception:
            return None

    def generate_insights(self, user_stats):
        """
        Returns a markdown analysis string of the user's learning habits, or an error message.
        """
        total = user_stats.get('total_contents', 0)
        by_status = user_stats.get('by_status', {})
        by_type = user_stats.get('by_type', [])

        status_lines = '\n'.join(
            f'  - {status}: {count}' for status, count in by_status.items()
        )
        type_lines = '\n'.join(
            f'  - {item.get("content_type", "unknown")}: {item.get("count", 0)}'
            for item in by_type
        )

        prompt = (
            f'Here are content consumption statistics for a learner:\n\n'
            f'Total contents: {total}\n\n'
            f'By status:\n{status_lines}\n\n'
            f'By type:\n{type_lines}\n\n'
            f'Provide a brief analysis (3-5 bullet points) of the user\'s learning habits '
            f'and 2-3 actionable suggestions to improve. '
            f'Format as markdown with **bold** headers. Keep it concise and encouraging.'
        )

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=500,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return response.content[0].text
        except anthropic.APIError:
            return None
        except anthropic.APIConnectionError:
            return None
        except anthropic.RateLimitError:
            return None
        except anthropic.APITimeoutError:
            return None
        except Exception:
            return None
