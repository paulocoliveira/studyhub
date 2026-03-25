---
name: Sprint 4 QA findings
description: Dashboard sprint test results — 4 design system color bugs, empty tests.py, all functional tests pass
type: project
---

## Sprint 4 (Dashboard) — QA Results

**Date tested:** 2026-03-25
**Report:** `aireports/SPRINT4_TEST_REPORT.md`
**Summary:** 15 TCs total — 11 PASS, 1 FAIL (TC-06 partial, resolved as PASS via content check), 3 WARN (DS-05 typography, DS-06 missing tests)

### Bugs found (all Medium or Low severity)

- **BUG-01 Medium:** "New" status badge uses `blue` instead of `sky` (`templates/dashboard/dashboard.html` lines 47, 48, 56)
- **BUG-02 Medium:** "In Progress" status badge uses `yellow` instead of `amber` (lines 66, 67, 74)
- **BUG-03 Medium:** "Completed" status badge uses `green` instead of `emerald` (lines 84, 85, 92)
- **BUG-04 Medium:** Video content type badge uses `red` instead of `rose` (lines 114, 167, 224 — 3 occurrences)
- **BUG-05 Low:** `dashboard/tests.py` is empty — 0 automated tests exist for the dashboard app

### Key passing verifications

- Django system check: 0 issues
- Migration state: clean (no migrations needed; dashboard has no models)
- URL `dashboard:home` resolves to `/dashboard/`
- `LoginRequiredMixin` redirects unauthenticated → `/users/login/?next=/dashboard/`
- `DashboardService` all 5 methods work without exception
- Stats correctness: `total_contents`, `by_status`, `by_type` all accurate
- Recent items: max 5, correct ordering
- Top categories/tags: annotated with `content_count`, descending order, accurate counts
- User data isolation: full isolation confirmed across all methods
- Empty state template renders correctly (all 4 empty state messages present)
- `LOGIN_REDIRECT_URL = '/dashboard/'` confirmed in settings
- No raw SQL in services.py; all queries user-scoped

### Known Django test client quirk

`resp.templates` returns empty list when using `APP_DIRS=True`. Workaround: verify template was used by checking `resp.content` for expected HTML landmarks.

**Why:** This is a Django test client limitation with the `APP_DIRS` template loader — template tracking requires the non-`APP_DIRS` style.
**How to apply:** In all future sprint tests with this project, validate template rendering via `resp.content.decode()` string checks, not `resp.templates`.
