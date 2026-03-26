import json
import time
from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from categories.models import Category
from contents.models import Content
from tags.models import Tag

from .services import AIService, build_user_context

User = get_user_model()


def make_user(email='insight@example.com', password='TestPass123!'):
    return User.objects.create_user(email=email, password=password)


def _json_post(client, url, data):
    return client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    )


# ---------------------------------------------------------------------------
# 9.5.1 — Authentication required
# ---------------------------------------------------------------------------

class InsightsAuthenticationRequiredTest(TestCase):
    def _assert_redirects_anonymous(self, url, method='post'):
        if method == 'post':
            response = _json_post(self.client, url, {'title': 'test'})
        else:
            response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_anonymous_post_suggest_category_redirects(self):
        self._assert_redirects_anonymous(reverse('insights:suggest_category'))

    def test_anonymous_post_generate_description_redirects(self):
        self._assert_redirects_anonymous(reverse('insights:generate_description'))

    def test_anonymous_get_generate_insights_redirects(self):
        self._assert_redirects_anonymous(reverse('insights:generate_insights'), method='get')


# ---------------------------------------------------------------------------
# 9.5.2 — Mocked AI success responses
# ---------------------------------------------------------------------------

class InsightsMockedSuccessTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        Category.objects.create(name='Technology', user=self.user)

    @patch('insights.views.AIService')
    def test_suggest_category_returns_200_with_category_key(self, MockAIService):
        instance = MockAIService.return_value
        instance.suggest_category.return_value = 'Technology'
        response = _json_post(
            self.client,
            reverse('insights:suggest_category'),
            {'title': 'Intro to Django'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('category', data)
        self.assertEqual(data['category'], 'Technology')

    @patch('insights.views.AIService')
    def test_generate_description_returns_200_with_description_key(self, MockAIService):
        instance = MockAIService.return_value
        instance.generate_description.return_value = 'A great article about Django.'
        response = _json_post(
            self.client,
            reverse('insights:generate_description'),
            {'title': 'Django for Beginners'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('description', data)
        self.assertEqual(data['description'], 'A great article about Django.')

    @patch('insights.views.AIService')
    def test_generate_insights_returns_200_with_insights_key(self, MockAIService):
        instance = MockAIService.return_value
        instance.generate_insights.return_value = '**Insight 1**: You read a lot.'
        response = self.client.get(reverse('insights:generate_insights'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('insights', data)


# ---------------------------------------------------------------------------
# 9.5.3 — AI failure (GenerateInsightsView)
# ---------------------------------------------------------------------------

class InsightsAIFailureTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    @patch('insights.views.AIService')
    def test_generate_insights_ai_returns_none_gives_503(self, MockAIService):
        instance = MockAIService.return_value
        instance.generate_insights.return_value = None
        response = self.client.get(reverse('insights:generate_insights'))
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


# ---------------------------------------------------------------------------
# 9.5.4 — SuggestCategoryView with no categories
# ---------------------------------------------------------------------------

class SuggestCategoryNoCategoriesTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def test_post_with_title_but_no_categories_returns_400(self):
        response = _json_post(
            self.client,
            reverse('insights:suggest_category'),
            {'title': 'Some Content Title'},
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


# ---------------------------------------------------------------------------
# 9.6.1 — SuggestNextView
# ---------------------------------------------------------------------------

class SuggestNextViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_anonymous_post_redirects(self):
        response = _json_post(self.client, reverse('insights:suggest_next'), {})
        self.assertEqual(response.status_code, 302)

    @patch('insights.views.AIService')
    def test_authenticated_post_mocked_success_returns_html_key(self, MockAIService):
        self.client.force_login(self.user)
        instance = MockAIService.return_value
        instance.suggest_next.return_value = '1. Read Python docs'
        response = _json_post(self.client, reverse('insights:suggest_next'), {})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('html', data)

    @patch('insights.views.AIService')
    def test_authenticated_post_ai_returns_none_gives_503(self, MockAIService):
        self.client.force_login(self.user)
        instance = MockAIService.return_value
        instance.suggest_next.return_value = None
        response = _json_post(self.client, reverse('insights:suggest_next'), {})
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


# ---------------------------------------------------------------------------
# 9.6.2 — ForgottenContentsView
# ---------------------------------------------------------------------------

class ForgottenContentsViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_anonymous_get_redirects(self):
        response = self.client.get(reverse('insights:forgotten_contents'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_get_content_older_than_30_days_returned(self):
        self.client.force_login(self.user)
        old_content = Content.objects.create(
            user=self.user,
            title='Old Forgotten Article',
            content_type='article',
            status='new',
        )
        # Bypass auto_now_add by using update() on the queryset
        old_date = timezone.now() - timedelta(days=35)
        Content.objects.filter(pk=old_content.pk).update(created_at=old_date)

        response = self.client.get(reverse('insights:forgotten_contents'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        ids = [item['id'] for item in data['items']]
        self.assertIn(old_content.pk, ids)

    def test_authenticated_get_content_newer_than_30_days_not_returned(self):
        self.client.force_login(self.user)
        Content.objects.create(
            user=self.user,
            title='Recent Article',
            content_type='article',
            status='new',
        )
        # created_at defaults to now, so it is < 30 days old
        response = self.client.get(reverse('insights:forgotten_contents'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        titles = [item['title'] for item in data['items']]
        self.assertNotIn('Recent Article', titles)

    def test_authenticated_get_completed_items_older_than_30_days_not_returned(self):
        self.client.force_login(self.user)
        completed_content = Content.objects.create(
            user=self.user,
            title='Old Completed',
            content_type='article',
            status='completed',
        )
        old_date = timezone.now() - timedelta(days=40)
        Content.objects.filter(pk=completed_content.pk).update(created_at=old_date)

        response = self.client.get(reverse('insights:forgotten_contents'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        titles = [item['title'] for item in data['items']]
        self.assertNotIn('Old Completed', titles)


# ---------------------------------------------------------------------------
# 9.6.3 — AnalyzeTopicsView
# ---------------------------------------------------------------------------

class AnalyzeTopicsViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_anonymous_post_redirects(self):
        response = _json_post(self.client, reverse('insights:analyze_topics'), {})
        self.assertEqual(response.status_code, 302)

    @patch('insights.views.AIService')
    def test_authenticated_post_mocked_success_returns_html_key(self, MockAIService):
        self.client.force_login(self.user)
        # Create a category with content so analyze_topics has data
        cat = Category.objects.create(name='Python', user=self.user)
        Content.objects.create(
            user=self.user, title='Python Basics', content_type='article',
            status='new', category=cat,
        )
        instance = MockAIService.return_value
        instance.analyze_topics.return_value = 'You focus on Python. 1. Go deeper.'
        response = _json_post(self.client, reverse('insights:analyze_topics'), {})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('html', data)


# ---------------------------------------------------------------------------
# 9.6.4 — WeeklySummaryView
# ---------------------------------------------------------------------------

class WeeklySummaryViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_anonymous_post_redirects(self):
        response = _json_post(self.client, reverse('insights:weekly_summary'), {})
        self.assertEqual(response.status_code, 302)

    @patch('insights.views.AIService')
    def test_authenticated_post_mocked_success_returns_html_key(self, MockAIService):
        self.client.force_login(self.user)
        instance = MockAIService.return_value
        instance.weekly_summary.return_value = 'Great week! You completed 2 items.'
        response = _json_post(self.client, reverse('insights:weekly_summary'), {})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('html', data)


# ---------------------------------------------------------------------------
# 9.6.5 — ChatView
# ---------------------------------------------------------------------------

class ChatViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_anonymous_post_redirects(self):
        response = _json_post(
            self.client, reverse('insights:chat'), {'message': 'hello', 'history': []}
        )
        self.assertEqual(response.status_code, 302)

    @patch('insights.views.AIService')
    def test_authenticated_post_with_message_and_history_returns_reply(self, MockAIService):
        self.client.force_login(self.user)
        instance = MockAIService.return_value
        instance.chat.return_value = 'You have 5 items in your library.'
        response = _json_post(
            self.client,
            reverse('insights:chat'),
            {'message': 'hello', 'history': []},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('reply', data)
        self.assertEqual(data['reply'], 'You have 5 items in your library.')

    def test_authenticated_post_empty_message_returns_400(self):
        self.client.force_login(self.user)
        response = _json_post(
            self.client,
            reverse('insights:chat'),
            {'message': '', 'history': []},
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    @patch('insights.views.AIService')
    def test_authenticated_post_ai_returns_none_gives_503(self, MockAIService):
        self.client.force_login(self.user)
        instance = MockAIService.return_value
        instance.chat.return_value = None
        response = _json_post(
            self.client,
            reverse('insights:chat'),
            {'message': 'What should I study?', 'history': []},
        )
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


# ---------------------------------------------------------------------------
# 9.6.6 — ChatView rate limiting
# ---------------------------------------------------------------------------

class ChatViewRateLimitTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    @patch('insights.views.AIService')
    def test_exceeding_daily_chat_limit_returns_429(self, MockAIService):
        instance = MockAIService.return_value
        instance.chat.return_value = 'A reply'

        # Simulate having already used the full daily limit in the session
        from insights.views import ChatView
        session = self.client.session
        session['ai_rate_chat_count'] = ChatView.DAILY_CHAT_LIMIT
        session['ai_rate_chat_window'] = time.time()
        session.save()

        response = _json_post(
            self.client,
            reverse('insights:chat'),
            {'message': 'One more message', 'history': []},
        )
        self.assertEqual(response.status_code, 429)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


# ---------------------------------------------------------------------------
# 9.6.7 — build_user_context
# ---------------------------------------------------------------------------

class BuildUserContextTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat = Category.objects.create(name='Machine Learning', user=self.user)
        self.content = Content.objects.create(
            user=self.user,
            title='Intro to Neural Networks',
            content_type='article',
            status='new',
            category=self.cat,
        )

    def test_build_user_context_returns_non_empty_string(self):
        context = build_user_context(self.user)
        self.assertIsInstance(context, str)
        self.assertTrue(len(context) > 0)

    def test_build_user_context_contains_content_title(self):
        context = build_user_context(self.user)
        self.assertIn('Intro to Neural Networks', context)

    def test_build_user_context_contains_category_name(self):
        context = build_user_context(self.user)
        self.assertIn('Machine Learning', context)

    def test_build_user_context_contains_total_count(self):
        # Add a second content item to make the count clear
        Content.objects.create(
            user=self.user,
            title='Advanced Deep Learning',
            content_type='course',
            status='in_progress',
        )
        context = build_user_context(self.user)
        self.assertIn('Total items: 2', context)


# ---------------------------------------------------------------------------
# Bug verification tests — PASS when bug is present, FAIL when bug is fixed
# ---------------------------------------------------------------------------


class BugVerificationTests(TestCase):
    # ------------------------------------------------------------------
    # Bug 10.1.19 — suggest_category passes all users' categories to AI
    # ------------------------------------------------------------------
    def test_bug_10_1_19_suggest_category_uses_all_categories(self):
        user1 = User.objects.create_user(
            email='user1@insightbug.com', password='TestPass123!'
        )
        user2 = User.objects.create_user(
            email='user2@insightbug.com', password='TestPass123!'
        )

        Category.objects.create(name='AI', user=user1)
        Category.objects.create(name='DevOps', user=user2)

        self.client.force_login(user1)

        with patch('insights.views.AIService') as MockAIService:
            instance = MockAIService.return_value
            instance.suggest_category.return_value = 'AI'

            _json_post(
                self.client,
                reverse('insights:suggest_category'),
                {'title': 'Kubernetes intro'},
            )

            self.assertTrue(instance.suggest_category.called)
            call_args = instance.suggest_category.call_args
            # The third positional argument is the list of category names
            category_names_passed = call_args[0][2]

            # Bug present: category_names_passed contains user2's 'DevOps' category
            # because the view uses Category.objects.all() instead of
            # Category.objects.filter(user=request.user)
            self.assertIn('DevOps', category_names_passed)
