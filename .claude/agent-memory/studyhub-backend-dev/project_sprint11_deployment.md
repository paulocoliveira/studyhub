---
name: Sprint 11 Deployment Preparation
description: Deployment prep — Docker, whitenoise, env-based settings, requirements.txt, README, CHANGELOG
type: project
---

Sprint 11 added production deployment scaffolding. Key facts:

- `requirements.txt` now includes gunicorn==23.0.0, whitenoise==6.9.0 (and all pinned transitive deps)
- `core/settings.py` reads SECRET_KEY, DEBUG, ALLOWED_HOSTS from env vars; ALLOWED_HOSTS splits on commas
- `whitenoise.middleware.WhiteNoiseMiddleware` inserted immediately after SecurityMiddleware
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` added; `STATICFILES_STORAGE` set to CompressedManifestStaticFilesStorage
- `staticfiles/` directory populated via `collectstatic --noinput` (137 files)
- Dockerfile, docker-compose.yml, .dockerignore, .env.example, README.md, CHANGELOG.md created at project root
- dashboard/services.py and insights/views.py received inline comments (task 11.4.2)

**Why:** `dashboard/services.py get_stats()` still uses `Content.objects.count()` (global, not user-scoped) — this is a pre-existing known bug from sprint 10; do NOT change it to `base_qs.count()` without also updating the bug-verification test `test_bug_10_1_15_total_count_includes_all_users`.

**How to apply:** Sprint 11 changes introduced no new test failures. Pre-sprint baseline was 9 failures + 1 error (88 tests total), which remains unchanged after sprint 11.
