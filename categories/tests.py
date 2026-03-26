from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from contents.models import Content

from .models import Category

User = get_user_model()


def make_user(email='user@example.com', password='TestPass123!'):
    return User.objects.create_user(email=email, password=password)


def make_category(user, name='Tech'):
    return Category.objects.create(name=name, user=user)


class CategoryCRUDTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def test_create_category_saved_and_appears_in_list(self):
        response = self.client.post(
            reverse('categories:create'),
            {'name': 'Science', 'description': 'Science stuff'},
        )
        self.assertRedirects(response, reverse('categories:list'))
        self.assertTrue(Category.objects.filter(name='Science', user=self.user).exists())
        list_response = self.client.get(reverse('categories:list'))
        self.assertEqual(list_response.status_code, 200)
        names = [c.name for c in list_response.context['categories']]
        self.assertIn('Science', names)

    def test_edit_category_changes_are_saved(self):
        cat = make_category(self.user, name='OldName')
        response = self.client.post(
            reverse('categories:update', kwargs={'pk': cat.pk}),
            {'name': 'NewName', 'description': ''},
        )
        self.assertRedirects(response, reverse('categories:list'))
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'NewName')

    def test_delete_category_removes_it_and_nullifies_content_category(self):
        cat = make_category(self.user, name='ToDelete')
        content = Content.objects.create(
            user=self.user,
            title='Content in Category',
            content_type='article',
            status='new',
            category=cat,
        )
        response = self.client.post(
            reverse('categories:delete', kwargs={'pk': cat.pk})
        )
        self.assertRedirects(response, reverse('categories:list'))
        self.assertFalse(Category.objects.filter(pk=cat.pk).exists())
        content.refresh_from_db()
        self.assertIsNone(content.category)
        # Content itself must NOT be deleted
        self.assertTrue(Content.objects.filter(pk=content.pk).exists())


class CategoryDataIsolationTest(TestCase):
    def setUp(self):
        self.user_a = make_user('catusera@example.com')
        self.user_b = make_user('catuserb@example.com')
        self.cat_a = make_category(self.user_a, 'CatA')
        self.cat_b = make_category(self.user_b, 'CatB')

    def test_user_a_cannot_see_user_b_categories(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('categories:list'))
        names = [c.name for c in response.context['categories']]
        self.assertIn('CatA', names)
        self.assertNotIn('CatB', names)

    def test_user_a_cannot_edit_user_b_category(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('categories:update', kwargs={'pk': self.cat_b.pk}),
            {'name': 'HackedName', 'description': ''},
        )
        self.assertEqual(response.status_code, 404)
        self.cat_b.refresh_from_db()
        self.assertEqual(self.cat_b.name, 'CatB')

    def test_user_a_cannot_delete_user_b_category(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('categories:delete', kwargs={'pk': self.cat_b.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Category.objects.filter(pk=self.cat_b.pk).exists())


class CategoryDuplicateNameTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        make_category(self.user, name='Duplicate')

    def test_duplicate_category_name_for_same_user_raises_integrity_error(self):
        # The CategoryForm does not include the user field, so the unique_together
        # constraint (name + user) is enforced at the database level rather than via
        # form validation. A second POST with the same name raises IntegrityError.
        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse('categories:create'),
                {'name': 'Duplicate', 'description': ''},
            )
