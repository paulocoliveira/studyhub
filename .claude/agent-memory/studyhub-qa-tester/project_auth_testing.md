---
name: StudyHub auth testing workarounds
description: Client.login() fails with EmailBackend — use force_login(); response.context is None outside TestCase
type: project
---

Django's `Client.login(email=..., password=...)` returns `False` for all users because the custom `users.backends.EmailBackend` is not compatible with how `Client.login()` internally authenticates. Always use `client.force_login(user)` in shell-based test scripts.

**Why:** The project uses `AUTH_USER_MODEL = 'users.CustomUser'` with `USERNAME_FIELD = 'email'` and `AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']`. Django's test client `login()` uses `ModelBackend` internally, not the configured backend.

**How to apply:** Any test script run via `python manage.py shell < script.py` must create users with `User.objects.create_user(...)` and authenticate with `client.force_login(user)`. Never use `client.login(email=..., password=...)` — it will silently fail and all authenticated-only requests will 302 to login.

Additionally: `response.context` is always `None` when `Client` is used inside `manage.py shell`. Context inspection only works inside `django.test.TestCase`. For shell-based testing, verify filter/queryset correctness by inspecting the HTML response body (check for presence/absence of specific text) or by running ORM queries that mirror the view's `get_queryset()` logic.
