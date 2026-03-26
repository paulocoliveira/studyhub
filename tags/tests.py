from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from contents.models import Content

from .models import Tag

User = get_user_model()


def make_user(email='user@example.com', password='TestPass123!'):
    return User.objects.create_user(email=email, password=password)


def make_tag(user, name='python'):
    return Tag.objects.create(name=name, user=user)


class TagCRUDTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def test_create_tag_saved_and_appears_in_list(self):
        response = self.client.post(
            reverse('tags:create'),
            {'name': 'django'},
        )
        self.assertRedirects(response, reverse('tags:list'))
        self.assertTrue(Tag.objects.filter(name='django', user=self.user).exists())
        list_response = self.client.get(reverse('tags:list'))
        self.assertEqual(list_response.status_code, 200)
        names = [t.name for t in list_response.context['tags']]
        self.assertIn('django', names)

    def test_delete_tag_removes_it_and_content_not_deleted(self):
        tag = make_tag(self.user, name='removeme')
        content = Content.objects.create(
            user=self.user,
            title='Tagged Content',
            content_type='article',
            status='new',
        )
        content.tags.add(tag)
        response = self.client.post(
            reverse('tags:delete', kwargs={'pk': tag.pk})
        )
        self.assertRedirects(response, reverse('tags:list'))
        self.assertFalse(Tag.objects.filter(pk=tag.pk).exists())
        # Content must still exist
        self.assertTrue(Content.objects.filter(pk=content.pk).exists())
        # Content should no longer reference the deleted tag
        self.assertNotIn(tag.pk, content.tags.values_list('pk', flat=True))


class TagDataIsolationTest(TestCase):
    def setUp(self):
        self.user_a = make_user('tagusera@example.com')
        self.user_b = make_user('taguserb@example.com')
        self.tag_a = make_tag(self.user_a, 'TagA')
        self.tag_b = make_tag(self.user_b, 'TagB')

    def test_user_a_cannot_see_user_b_tags(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('tags:list'))
        names = [t.name for t in response.context['tags']]
        self.assertIn('TagA', names)
        self.assertNotIn('TagB', names)

    def test_user_a_cannot_delete_user_b_tag(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('tags:delete', kwargs={'pk': self.tag_b.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tag.objects.filter(pk=self.tag_b.pk).exists())


class TagDuplicateNameTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        make_tag(self.user, name='duplicate')

    def test_duplicate_tag_name_for_same_user_raises_integrity_error(self):
        # The TagForm does not include the user field, so the unique_together constraint
        # (name + user) is enforced at the database level rather than via form validation.
        # A second POST with the same name raises IntegrityError.
        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse('tags:create'),
                {'name': 'duplicate'},
            )
