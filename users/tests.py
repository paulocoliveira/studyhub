import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegistrationTest(TestCase):
    def test_valid_registration_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'email': 'newuser@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'password1': 'SuperSecret123!',
                'password2': 'SuperSecret123!',
            },
        )
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_duplicate_email_shows_form_error_and_no_new_user(self):
        User.objects.create_user(email='existing@example.com', password='Pass123!')
        response = self.client.post(
            reverse('users:register'),
            {
                'email': 'existing@example.com',
                'password1': 'SuperSecret123!',
                'password2': 'SuperSecret123!',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'email',
            'User with this Email already exists.',
        )
        self.assertEqual(User.objects.filter(email='existing@example.com').count(), 1)

    def test_mismatched_passwords_shows_form_error_and_no_new_user(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'email': 'mismatch@example.com',
                'password1': 'SuperSecret123!',
                'password2': 'DifferentPassword!',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'password2',
            'The two password fields didn\u2019t match.',
        )
        self.assertFalse(User.objects.filter(email='mismatch@example.com').exists())


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='loginuser@example.com', password='ValidPass123!'
        )

    def test_correct_credentials_login_and_redirect_to_dashboard(self):
        response = self.client.post(
            reverse('users:login'),
            {'username': 'loginuser@example.com', 'password': 'ValidPass123!'},
        )
        self.assertRedirects(response, reverse('dashboard:home'))

    def test_wrong_password_login_fails_stays_on_login(self):
        response = self.client.post(
            reverse('users:login'),
            {'username': 'loginuser@example.com', 'password': 'WrongPassword!'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_nonexistent_email_login_fails_stays_on_login(self):
        response = self.client.post(
            reverse('users:login'),
            {'username': 'nobody@example.com', 'password': 'SomePass123!'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AccessControlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='authuser@example.com', password='ValidPass123!'
        )

    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_redirected_from_dashboard(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


class UserSettingsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='settings@example.com',
            password='ValidPass123!',
            ai_provider='anthropic',
            ai_api_key='sk-existing-key',
        )

    def test_post_valid_ai_settings_saves_correctly(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:settings'),
            {'ai_provider': 'openai', 'ai_api_key': 'sk-new-openai-key'},
        )
        self.assertRedirects(response, reverse('users:settings'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.ai_provider, 'openai')
        self.assertEqual(self.user.ai_api_key, 'sk-new-openai-key')

    def test_post_blank_ai_api_key_preserves_existing_key(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:settings'),
            {'ai_provider': 'anthropic', 'ai_api_key': ''},
        )
        self.assertRedirects(response, reverse('users:settings'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.ai_api_key, 'sk-existing-key')


# ---------------------------------------------------------------------------
# Bug verification tests — PASS when bug is present, FAIL when bug is fixed
# ---------------------------------------------------------------------------


class BugVerificationTests(TestCase):
    # ------------------------------------------------------------------
    # Bug 10.1.1 — Short password accepted (MinimumLengthValidator absent)
    # ------------------------------------------------------------------
    def test_bug_10_1_1_short_password_accepted(self):
        # A 2-character password should fail validation but the
        # MinimumLengthValidator is missing from AUTH_PASSWORD_VALIDATORS,
        # so registration succeeds and returns a redirect (302).
        response = self.client.post(
            reverse('users:register'),
            {
                'email': 'shortpass@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'password1': 'ab',
                'password2': 'ab',
            },
        )
        # Bug present: registration succeeds with a weak password → redirect
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Bug 10.1.2 — Login reveals whether an email account exists
    # ------------------------------------------------------------------
    def test_bug_10_1_2_login_reveals_email_existence(self):
        User.objects.create_user(email='existing@test.com', password='ValidPass123!')

        # Wrong password for a real account
        response_existing = self.client.post(
            reverse('users:login'),
            {'username': 'existing@test.com', 'password': 'wrongpassword'},
        )
        content_existing = response_existing.content.decode()

        # Wrong password for a non-existent account
        response_missing = self.client.post(
            reverse('users:login'),
            {'username': 'notexisting@test.com', 'password': 'wrongpassword'},
        )
        content_missing = response_missing.content.decode()

        # Bug present: each branch emits a distinct message leaking account existence
        self.assertIn('incorrect', content_existing.lower())
        self.assertIn('found', content_missing.lower())
        self.assertNotEqual(content_existing, content_missing)

    # ------------------------------------------------------------------
    # Bug 10.1.3 — Password change invalidates session (missing update_session_auth_hash)
    # ------------------------------------------------------------------
    def test_bug_10_1_3_password_change_invalidates_session(self):
        user = User.objects.create_user(
            email='changepass@example.com', password='OldPassword123!'
        )
        self.client.force_login(user)

        self.client.post(
            reverse('users:password_change'),
            {
                'old_password': 'OldPassword123!',
                'new_password1': 'NewPassword456!',
                'new_password2': 'NewPassword456!',
            },
        )

        # Bug present: session is invalidated because update_session_auth_hash
        # was not called, so the protected page redirects to login (302).
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])
