import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from tags.models import Tag

from .models import Content

User = get_user_model()


def make_user(email='user@example.com', password='TestPass123!'):
    return User.objects.create_user(email=email, password=password)


def make_content(user, title='Test Content', content_type='article', status='new', **kwargs):
    return Content.objects.create(
        user=user,
        title=title,
        content_type=content_type,
        status=status,
        **kwargs,
    )


class ContentCreateTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def test_valid_data_creates_content_and_redirects(self):
        response = self.client.post(
            reverse('contents:create'),
            {
                'title': 'My New Article',
                'content_type': 'article',
                'status': 'new',
                'description': '',
                'url': '',
            },
        )
        self.assertRedirects(response, reverse('contents:list'))
        self.assertTrue(Content.objects.filter(title='My New Article', user=self.user).exists())

    def test_missing_title_shows_form_error_no_content_saved(self):
        response = self.client.post(
            reverse('contents:create'),
            {'title': '', 'content_type': 'article', 'status': 'new'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title', 'This field is required.')
        self.assertEqual(Content.objects.filter(user=self.user).count(), 0)

    def test_missing_content_type_shows_form_error_no_content_saved(self):
        response = self.client.post(
            reverse('contents:create'),
            {'title': 'No Type Content', 'content_type': '', 'status': 'new'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'content_type', 'This field is required.')
        self.assertEqual(Content.objects.filter(user=self.user).count(), 0)


class ContentDataIsolationTest(TestCase):
    def setUp(self):
        self.user_a = make_user('usera@example.com')
        self.user_b = make_user('userb@example.com')
        self.content_a = make_content(self.user_a, title='A Article')
        self.content_b = make_content(self.user_b, title='B Article')

    def test_user_a_can_see_own_content_list(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('contents:list'))
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('A Article', titles)
        self.assertNotIn('B Article', titles)

    def test_user_a_cannot_access_user_b_detail(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('contents:detail', kwargs={'pk': self.content_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_access_user_b_edit(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('contents:update', kwargs={'pk': self.content_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_access_user_b_delete(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('contents:delete', kwargs={'pk': self.content_b.pk})
        )
        self.assertEqual(response.status_code, 404)


class ContentStatusUpdateAndDeleteTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        self.content = make_content(self.user, status='new')

    def test_post_valid_status_update_changes_status_and_redirects(self):
        response = self.client.post(
            reverse('contents:status_update', kwargs={'pk': self.content.pk}),
            {'status': 'in_progress'},
            HTTP_REFERER=reverse('contents:list'),
        )
        self.assertEqual(response.status_code, 302)
        self.content.refresh_from_db()
        self.assertEqual(self.content.status, 'in_progress')

    def test_post_delete_removes_content_and_redirects_to_list(self):
        pk = self.content.pk
        response = self.client.post(
            reverse('contents:delete', kwargs={'pk': pk})
        )
        self.assertRedirects(response, reverse('contents:list'))
        self.assertFalse(Content.objects.filter(pk=pk).exists())


class ContentFilteringTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        self.cat = Category.objects.create(name='Tech', user=self.user)
        make_content(self.user, title='New Article', content_type='article', status='new')
        make_content(self.user, title='In Progress Video', content_type='video', status='in_progress')
        make_content(
            self.user,
            title='Completed Article',
            content_type='article',
            status='completed',
            category=self.cat,
        )

    def test_filter_by_status_new_returns_only_new_items(self):
        response = self.client.get(reverse('contents:list'), {'status': 'new'})
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('New Article', titles)
        self.assertNotIn('In Progress Video', titles)
        self.assertNotIn('Completed Article', titles)

    def test_filter_by_status_completed_with_show_completed_returns_only_completed(self):
        response = self.client.get(
            reverse('contents:list'), {'status': 'completed', 'show_completed': '1'}
        )
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('Completed Article', titles)
        self.assertNotIn('New Article', titles)
        self.assertNotIn('In Progress Video', titles)

    def test_filter_by_content_type_video_returns_only_videos(self):
        response = self.client.get(reverse('contents:list'), {'content_type': 'video'})
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('In Progress Video', titles)
        self.assertNotIn('New Article', titles)

    def test_filter_by_category_returns_only_that_category(self):
        response = self.client.get(
            reverse('contents:list'),
            {'category': self.cat.pk, 'show_completed': '1'},
        )
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('Completed Article', titles)
        self.assertNotIn('New Article', titles)
        self.assertNotIn('In Progress Video', titles)


class ContentSearchTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        make_content(self.user, title='Python Tutorial', content_type='article')
        make_content(self.user, title='JavaScript Guide', content_type='article')

    def test_search_by_partial_title_returns_matching_items(self):
        response = self.client.get(reverse('contents:list'), {'search': 'Python'})
        self.assertEqual(response.status_code, 200)
        titles = [c.title for c in response.context['contents']]
        self.assertIn('Python Tutorial', titles)
        self.assertNotIn('JavaScript Guide', titles)

    def test_search_with_no_matches_returns_empty_results(self):
        response = self.client.get(reverse('contents:list'), {'search': 'RustLang'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contents']), 0)


class ContentFileUploadTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def _post_with_file(self, filename, content=b'data', size=None):
        if size is not None:
            file_content = b'x' * size
        else:
            file_content = content
        uploaded = SimpleUploadedFile(filename, file_content)
        return self.client.post(
            reverse('contents:create'),
            {
                'title': 'Upload Test',
                'content_type': 'article',
                'status': 'new',
                'file': uploaded,
            },
        )

    def test_upload_allowed_extension_pdf_is_accepted(self):
        response = self._post_with_file('document.pdf', b'%PDF-1.4 content')
        self.assertRedirects(response, reverse('contents:list'))
        self.assertTrue(
            Content.objects.filter(user=self.user, title='Upload Test').exists()
        )

    def test_upload_disallowed_extension_shows_form_error(self):
        response = self._post_with_file('malware.exe', b'MZ binary')
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertFalse(
            Content.objects.filter(user=self.user, title='Upload Test').exists()
        )

    def test_upload_exceeding_10mb_shows_form_error(self):
        over_limit = 10 * 1024 * 1024 + 1
        response = self._post_with_file('bigfile.pdf', size=over_limit)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertFalse(
            Content.objects.filter(user=self.user, title='Upload Test').exists()
        )


# ---------------------------------------------------------------------------
# Bug verification tests — PASS when bug is present, FAIL when bug is fixed
# ---------------------------------------------------------------------------


class BugVerificationTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    # ------------------------------------------------------------------
    # Bug 10.1.7 — sort=created_at (oldest first) uses same order as newest
    # ------------------------------------------------------------------
    def test_bug_10_1_7_oldest_sort_same_as_newest(self):
        import datetime
        from django.utils import timezone

        c1 = make_content(self.user, title='Alpha', content_type='article', status='new')
        c2 = make_content(self.user, title='Beta', content_type='article', status='new')
        c3 = make_content(self.user, title='Gamma', content_type='article', status='new')

        now = timezone.now()
        Content.objects.filter(pk=c1.pk).update(
            created_at=now - datetime.timedelta(days=10)
        )
        Content.objects.filter(pk=c2.pk).update(
            created_at=now - datetime.timedelta(days=5)
        )
        Content.objects.filter(pk=c3.pk).update(
            created_at=now - datetime.timedelta(days=1)
        )

        response_oldest = self.client.get(
            reverse('contents:list'), {'sort': 'created_at'}
        )
        response_newest = self.client.get(
            reverse('contents:list'), {'sort': '-created_at'}
        )

        titles_oldest = [c.title for c in response_oldest.context['contents']]
        titles_newest = [c.title for c in response_newest.context['contents']]

        # Bug present: both orderings produce identical results
        self.assertEqual(titles_oldest, titles_newest)

    # ------------------------------------------------------------------
    # Bug 10.1.8 — mark completed saves in_progress instead
    # ------------------------------------------------------------------
    def test_bug_10_1_8_mark_completed_saves_in_progress(self):
        content = make_content(self.user, status='new')
        self.client.post(
            reverse('contents:status_update', kwargs={'pk': content.pk}),
            {'status': 'completed'},
            HTTP_REFERER=reverse('contents:list'),
        )
        content.refresh_from_db()
        # Bug present: status is saved as in_progress, not completed
        self.assertEqual(content.status, 'in_progress')

    # ------------------------------------------------------------------
    # Bug 10.1.9 — total_count ignores active filters
    # ------------------------------------------------------------------
    def test_bug_10_1_9_total_count_ignores_filter(self):
        for i in range(5):
            make_content(
                self.user,
                title=f'New Item {i}',
                content_type='article',
                status='new',
            )
        make_content(
            self.user,
            title='Completed Item',
            content_type='article',
            status='completed',
        )

        response = self.client.get(
            reverse('contents:list'),
            {'status': 'completed', 'show_completed': '1'},
        )
        total_count = response.context['total_count']
        # Bug present: total_count reflects all 6 items regardless of filter
        self.assertEqual(total_count, 6)

    # ------------------------------------------------------------------
    # Bug 10.1.17 — create content flashes an ERROR message instead of SUCCESS
    # ------------------------------------------------------------------
    def test_bug_10_1_17_create_content_uses_error_message(self):
        from django.contrib.messages import constants as message_constants

        response = self.client.post(
            reverse('contents:create'),
            {
                'title': 'My New Content',
                'content_type': 'article',
                'status': 'new',
                'description': '',
                'url': '',
            },
            follow=True,
        )
        msgs = list(response.context['messages'])
        self.assertTrue(len(msgs) > 0)
        # Bug present: the message level is ERROR (40) instead of SUCCESS (25)
        self.assertEqual(msgs[0].level, message_constants.ERROR)
