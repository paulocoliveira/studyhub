# Sprint 4 — Bug Report
## StudyHub — Dashboard

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 5
**Fixed:** 4 (during QA)
**Pending:** 1 (Sprint 7)

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Medium | `templates/dashboard/dashboard.html` | Fixed |
| [B-02](#b-02) | Medium | `templates/dashboard/dashboard.html` | Fixed |
| [B-03](#b-03) | Medium | `templates/dashboard/dashboard.html` | Fixed |
| [B-04](#b-04) | Medium | `templates/dashboard/dashboard.html` | Fixed |
| [B-05](#b-05) | Low | `dashboard/tests.py` | Pending — Sprint 7 |

---

## B-01

**Title:** "New" status badge uses wrong Tailwind color (`blue` instead of `sky`)

**Severity:** Medium
**Component:** `templates/dashboard/dashboard.html`
**Status:** Fixed
**Discovered in:** TC-DS-01 (design system compliance review)
**Fix date:** 2026-03-25

### Description

The "New" status stat card on the dashboard used Tailwind `blue-*` color classes instead of the design-system-mandated `sky-*` color tokens. This caused a visual inconsistency with status badges used in `content_list.html` and the design system specification.

### Steps to reproduce

1. Log in and navigate to `/dashboard/`
2. Observe the "New" stat card
3. Inspect element — badge rendered with `bg-blue-500/10 text-blue-400`

### Expected behavior

Badge renders with `bg-sky-500/10 text-sky-400 border border-sky-500/20` per the design system Status Badges specification.

### Actual behavior

```html
<span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 ...">New</span>
```

### Root cause

The dashboard template was authored independently and used `blue` (a visually similar but incorrect Tailwind palette) instead of `sky`, which is the exact token defined in the design system for the "new" status.

### Fix applied

**File:** `templates/dashboard/dashboard.html`

```
# Before
bg-blue-500/10 text-blue-400 border border-blue-500/20

# After
bg-sky-500/10 text-sky-400 border border-sky-500/20
```

### Impact

Visual inconsistency: the "New" status color on the dashboard did not match the same status badge on the content list page, making the UI feel inconsistent.

---

## B-02

**Title:** "In Progress" status badge uses wrong Tailwind color (`yellow` instead of `amber`)

**Severity:** Medium
**Component:** `templates/dashboard/dashboard.html`
**Status:** Fixed
**Discovered in:** TC-DS-02 (design system compliance review)
**Fix date:** 2026-03-25

### Description

The "In Progress" status stat card used Tailwind `yellow-*` color classes instead of the design-system-mandated `amber-*` tokens, causing inconsistency with the rest of the application.

### Steps to reproduce

1. Log in and navigate to `/dashboard/`
2. Observe the "In Progress" stat card
3. Inspect element — badge rendered with `bg-yellow-500/10 text-yellow-400`

### Expected behavior

Badge renders with `bg-amber-500/10 text-amber-400 border border-amber-500/20`.

### Actual behavior

```html
<span class="bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 ...">In Progress</span>
```

### Root cause

Same as B-01 — `yellow` is visually close to `amber` but is a different Tailwind palette token. The design system explicitly defines `amber` for in-progress states.

### Fix applied

**File:** `templates/dashboard/dashboard.html`

```
# Before
bg-yellow-500/10 text-yellow-400 border border-yellow-500/20

# After
bg-amber-500/10 text-amber-400 border border-amber-500/20
```

### Impact

Visual inconsistency between the dashboard status cards and the content list status badges.

---

## B-03

**Title:** "Completed" status badge uses wrong Tailwind color (`green` instead of `emerald`)

**Severity:** Medium
**Component:** `templates/dashboard/dashboard.html`
**Status:** Fixed
**Discovered in:** TC-DS-03 (design system compliance review)
**Fix date:** 2026-03-25

### Description

The "Completed" status stat card used Tailwind `green-*` color classes instead of the design-system-mandated `emerald-*` tokens.

### Steps to reproduce

1. Log in and navigate to `/dashboard/`
2. Observe the "Completed" stat card
3. Inspect element — badge rendered with `bg-green-500/10 text-green-400`

### Expected behavior

Badge renders with `bg-emerald-500/10 text-emerald-400 border border-emerald-500/20`.

### Actual behavior

```html
<span class="bg-green-500/10 text-green-400 border border-green-500/20 ...">Completed</span>
```

### Root cause

`green` and `emerald` are distinct Tailwind palettes. The design system color token for "success/completed" states is `emerald`, not `green`.

### Fix applied

**File:** `templates/dashboard/dashboard.html`

```
# Before
bg-green-500/10 text-green-400 border border-green-500/20

# After
bg-emerald-500/10 text-emerald-400 border border-emerald-500/20
```

### Impact

Visual inconsistency: the "Completed" badge on the dashboard did not match the same badge on the content list and detail pages.

---

## B-04

**Title:** Video content type badge uses wrong Tailwind color (`red` instead of `rose`)

**Severity:** Medium
**Component:** `templates/dashboard/dashboard.html`
**Status:** Fixed
**Discovered in:** TC-DS-04 (design system compliance review)
**Fix date:** 2026-03-25

### Description

All three occurrences of the "Video" content type badge in the dashboard (Content Type Breakdown section, Recently Added list, Recently Completed list) used Tailwind `red-*` classes instead of the design-system-mandated `rose-*` tokens.

### Steps to reproduce

1. Log in, create a content item of type "Video"
2. Navigate to `/dashboard/`
3. Observe the Video badge in "Content by Type", "Recently Added", or "Recently Completed"
4. Inspect element — badge reads `bg-red-500/10 text-red-400`

### Expected behavior

Video badge renders with `bg-rose-500/10 text-rose-400` in all three sections.

### Actual behavior

```html
<span class="bg-red-500/10 text-red-400 ...">Video</span>
```

Three occurrences affected (content type breakdown, recently added, recently completed).

### Root cause

`red` and `rose` are distinct Tailwind palettes. The Content Type Badges section of the design system specifies `rose` for the "video" content type.

### Fix applied

**File:** `templates/dashboard/dashboard.html`

```
# Before (3 occurrences)
bg-red-500/10 text-red-400

# After
bg-rose-500/10 text-rose-400
```

### Impact

Visual inconsistency: the "Video" badge on the dashboard did not match the same badge on the content list and detail pages.

---

## B-05

**Title:** `dashboard/tests.py` is empty — no automated unit tests

**Severity:** Low
**Component:** `dashboard/tests.py`
**Status:** Pending — Sprint 7
**Discovered in:** TC-15 (automated test coverage review)
**Fix date:** Sprint 7

### Description

The `dashboard/tests.py` file was scaffolded but never populated. Running `python manage.py test dashboard` reports 0 tests. There is no regression coverage for `DashboardService` queries, `DashboardView` rendering, or user data isolation.

### Steps to reproduce

```bash
source .venv/bin/activate
python manage.py test dashboard --verbosity=2
# Output: Ran 0 tests in 0.000s — OK (no test cases)
```

### Expected behavior

At minimum, tests covering: `DashboardService` stat accuracy, user isolation, empty-state handling, and `DashboardView` HTTP response.

### Actual behavior

```
Ran 0 tests in 0.000s
OK
```

### Root cause

Sprint 4 focused on implementation. Sprint 7 is planned for the full testing pass across all apps.

### Fix

Write unit tests in `dashboard/tests.py` as part of Sprint 7.

### Impact

Without automated tests, any future refactor of the service layer or view can silently break dashboard data accuracy. Risk is low in early sprint but grows as complexity increases.

---

## Fix Summary

| ID | Modified file | Change | Migration needed |
|----|--------------|--------|-----------------|
| B-01 | `templates/dashboard/dashboard.html` | `blue-*` → `sky-*` on "New" status badge (3 tokens) | No |
| B-02 | `templates/dashboard/dashboard.html` | `yellow-*` → `amber-*` on "In Progress" status badge (3 tokens) | No |
| B-03 | `templates/dashboard/dashboard.html` | `green-*` → `emerald-*` on "Completed" status badge (3 tokens) | No |
| B-04 | `templates/dashboard/dashboard.html` | `red-*` → `rose-*` on Video content type badge (2 tokens × 3 occurrences) | No |
| B-05 | `dashboard/tests.py` | Write unit tests (Sprint 7) | No |
