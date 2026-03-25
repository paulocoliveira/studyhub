---
name: Sprint 1 QA findings
description: Key patterns and pitfalls discovered during Sprint 1 QA — auth flow, settings issues, test infrastructure gaps
type: project
---

Sprint 1 (2026-03-25) tested: project setup, TailwindCSS, custom user model, email-based auth, base templates, landing page.

All 20 functional tests passed. Two non-blocking issues found:

1. `ALLOWED_HOSTS = []` in `core/settings.py`. Django test `Client` from `manage.py shell` sends `HTTP_HOST: testserver`, which is rejected with `DisallowedHost` / HTTP 400. Must use `override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])` in any shell-based test scripts. The live dev server works because Django implicitly allows `127.0.0.1` in DEBUG mode.

2. `users/tests.py` is empty — only the auto-generated stub. No unit tests at all for the users app.

**Why:** These were not caught before because the dev server worked fine for manual testing, and no automated test infrastructure was in place yet.

**How to apply:** Always run shell test scripts with `override_settings` for `ALLOWED_HOSTS`. Flag missing test files in every sprint review.
