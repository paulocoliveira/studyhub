from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from contents.models import Content
from tags.models import Tag

from .services import DashboardService

User = get_user_model()


def make_user(email='dash@example.com', password='TestPass123!'):
    return User.objects.create_user(email=email, password=password)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_authenticated_get_dashboard_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_get_dashboard_redirects_to_login(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


class DashboardServiceStatsTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat1 = Category.objects.create(name='Programming', user=self.user)
        self.cat2 = Category.objects.create(name='Design', user=self.user)
        self.tag1 = Tag.objects.create(name='python', user=self.user)
        self.tag2 = Tag.objects.create(name='css', user=self.user)
        self.tag3 = Tag.objects.create(name='ux', user=self.user)

        # 3 new articles
        for i in range(3):
            c = Content.objects.create(
                user=self.user,
                title=f'New Article {i}',
                content_type='article',
                status='new',
                category=self.cat1,
            )
            c.tags.add(self.tag1)

        # 2 in_progress videos
        for i in range(2):
            c = Content.objects.create(
                user=self.user,
                title=f'In Progress Video {i}',
                content_type='video',
                status='in_progress',
                category=self.cat2,
            )
            c.tags.add(self.tag2)

        # 1 completed podcast
        c = Content.objects.create(
            user=self.user,
            title='Completed Podcast',
            content_type='podcast',
            status='completed',
        )
        c.tags.add(self.tag3)

        self.service = DashboardService(user=self.user)

    def test_total_contents_is_six(self):
        stats = self.service.get_stats()
        self.assertEqual(stats['total_contents'], 6)

    def test_by_status_counts_are_correct(self):
        stats = self.service.get_stats()
        self.assertEqual(stats['by_status']['new'], 3)
        self.assertEqual(stats['by_status']['in_progress'], 2)
        self.assertEqual(stats['by_status']['completed'], 1)

    def test_by_type_contains_correct_counts(self):
        stats = self.service.get_stats()
        by_type_map = {item['content_type']: item['count'] for item in stats['by_type']}
        self.assertEqual(by_type_map['article'], 3)
        self.assertEqual(by_type_map['video'], 2)
        self.assertEqual(by_type_map['podcast'], 1)

    def test_top_categories_ordered_by_content_count_descending(self):
        top_cats = list(self.service.get_top_categories())
        # Programming has 3 items, Design has 2 items
        self.assertEqual(top_cats[0].name, 'Programming')
        self.assertEqual(top_cats[0].content_count, 3)
        self.assertEqual(top_cats[1].name, 'Design')
        self.assertEqual(top_cats[1].content_count, 2)

    def test_top_tags_ordered_by_content_count_descending(self):
        top_tags = list(self.service.get_top_tags())
        tag_names = [t.name for t in top_tags]
        # python appears on 3 items, css on 2, ux on 1
        self.assertEqual(top_tags[0].name, 'python')
        self.assertEqual(top_tags[0].content_count, 3)
        self.assertIn('css', tag_names)
        self.assertIn('ux', tag_names)


class DashboardRecentListsTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other_user = make_user('other@example.com')

        # Create items in a known order
        self.content1 = Content.objects.create(
            user=self.user, title='First Added', content_type='article', status='new'
        )
        self.content2 = Content.objects.create(
            user=self.user, title='Second Added', content_type='article', status='new'
        )
        # Item belonging to another user
        Content.objects.create(
            user=self.other_user, title='Other User Content', content_type='article', status='new'
        )
        # Completed item for this user
        self.completed = Content.objects.create(
            user=self.user, title='Completed Item', content_type='article', status='completed'
        )

        self.service = DashboardService(user=self.user)

    def test_recently_added_ordered_by_created_at_descending_and_user_scoped(self):
        recent = list(self.service.get_recent_added())
        titles = [c.title for c in recent]
        # Most recently created should appear first
        self.assertEqual(titles[0], 'Completed Item')
        # Other user's content must not appear
        self.assertNotIn('Other User Content', titles)

    def test_recently_completed_only_completed_items_user_scoped(self):
        recent_completed = list(self.service.get_recent_completed())
        titles = [c.title for c in recent_completed]
        self.assertIn('Completed Item', titles)
        self.assertNotIn('First Added', titles)
        self.assertNotIn('Second Added', titles)
        self.assertNotIn('Other User Content', titles)

    def test_recently_completed_ordered_by_updated_at_descending(self):
        completed2 = Content.objects.create(
            user=self.user,
            title='Another Completed',
            content_type='article',
            status='completed',
        )
        recent_completed = list(self.service.get_recent_completed())
        # Most recently updated completed item should be first
        self.assertEqual(recent_completed[0].title, 'Another Completed')
