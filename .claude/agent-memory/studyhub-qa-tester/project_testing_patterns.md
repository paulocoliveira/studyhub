---
name: StudyHub QA testing patterns
description: Reliable testing patterns for StudyHub: test credentials, script setup, known flaky behaviors
type: project
---

## Test user
- Email: `test@studyhub.com`, password: `TestPass123!`
- Always clean up before and after: `User.objects.filter(email__in=['test@studyhub.com', ...]).delete()`

## Shell-based test scripts
Always wrap all `Client()` calls in `override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])`.
Without this, every request returns HTTP 400 due to `ALLOWED_HOSTS = []`.

Always instantiate `Client(raise_request_exception=False)` when testing for server error responses.
Without this flag, a view that throws an unhandled exception (e.g. FieldError → HTTP 500) will
re-raise the exception in the test client and crash the test script instead of returning a response
object with `status_code == 500`.

## Auth client setup
Use `client.login(username='test@studyhub.com', password='TestPass123!')` to authenticate the test client.
The `username` parameter maps to `email` because `USERNAME_FIELD = 'email'`.

## Dev server
Base URL: `http://127.0.0.1:8000`. Must start manually with `python manage.py runserver` (not auto-started).
The server must be running for Playwright tests; verify with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/`.

## Template naming
Public pages extend `base_public.html`. Authenticated pages extend `base.html`.
Sidebar and topbar are components in `templates/components/`.
