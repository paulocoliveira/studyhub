---
name: Sprint 9 Automated Tests
description: 78 tests across all apps; category/tag unique_together enforced at DB level not form level — raises IntegrityError on duplicate POSTs
type: project
---

Sprint 9 delivered 78 automated tests across all 6 apps (users, contents, categories, tags, dashboard, insights). All tests pass.

**Why:** Comprehensive test coverage was missing for all sprints 1-8 work.

**How to apply:** When adding new features, follow the established test patterns in each app's tests.py.

Key findings discovered during test writing:

- `CategoryForm` and `TagForm` do not include the `user` field, so `unique_together` constraint is not caught at form validation time — it surfaces as a raw `IntegrityError` at the DB level. Tests use `assertRaises(IntegrityError)` and avoid any DB queries after the exception (transaction is broken inside `TestCase`).
- `UserSettingsForm.clean_ai_api_key()` preserves the existing key when the submitted value is blank — this is intentional and tested.
- `ForgottenContentsView` uses `DashboardService.get_forgotten_contents(days=30)` which filters `status='new'` AND `created_at__lte=cutoff`. Tests manipulate `created_at` via `queryset.update()` to bypass `auto_now_add`.
- `ChatView.DAILY_CHAT_LIMIT = 20` — rate limit test sets session keys `ai_rate_chat_count` and `ai_rate_chat_window` directly.
- All insights views are JSON-only (no HTML forms); tests post via `content_type='application/json'`.
- Mock target is `'insights.views.AIService'` (where it is imported in views), not `'insights.services.AIService'`.
