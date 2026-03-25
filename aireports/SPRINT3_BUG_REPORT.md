# Sprint 3 — Bug Report
## StudyHub — Content Management

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 3
**Fixed:** 2 (during QA)
**Pending:** 1 (cosmetic, no functional impact)

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | High | `contents/views.py` | Fixed |
| [B-02](#b-02) | Low | `templates/contents/content_confirm_delete.html` | Fixed |
| [B-03](#b-03) | Low | `templates/contents/content_list.html`, `content_detail.html` | Deferred |

---

## B-01

**Title:** Search is non-functional — form submits `?search=` but view reads `?q=`

**Severity:** High
**Component:** `contents/views.py` — `ContentListView.get_queryset`
**Status:** Fixed
**Discovered in:** TC-11
**Fix date:** 2026-03-25

### Description

The `ContentFilterForm` defines a field named `search`, so the HTML form submits `GET ?search=<value>`. However, `ContentListView.get_queryset` read the search term with `request.GET.get('q', '')`. As a result, the search box appeared functional in the UI but returned all items regardless of what was typed.

### Steps to reproduce

```
1. Log in and navigate to /contents/
2. Type a search term in the search box
3. Click "Filter"
4. Observe: all contents shown, search term ignored
```

### Cause

```python
# BEFORE — reads wrong key
q = self.request.GET.get('q', '').strip()
```

The form field is named `search`, generating `?search=<value>`, but the view read `?q=`.

### Fix applied

**File:** `contents/views.py`

```python
# AFTER — reads the correct key matching the form field name
q = self.request.GET.get('search', '').strip()
```

### Impact

High: full-text search was completely broken for all users. No data loss, but a core filtering feature was non-operational.

---

## B-02

**Title:** Delete confirmation button uses wrong red variant

**Severity:** Low
**Component:** `templates/contents/content_confirm_delete.html`
**Status:** Fixed
**Discovered in:** Static analysis
**Fix date:** 2026-03-25

### Description

The delete confirmation button used `bg-red-600 hover:bg-red-700` instead of the design system rose variant (`bg-rose-600`) used consistently on delete buttons throughout the app (categories and tags confirm-delete pages).

### Fix applied

**File:** `templates/contents/content_confirm_delete.html`

```html
<!-- BEFORE -->
class='... bg-red-600 ... hover:bg-red-700 ...'

<!-- AFTER -->
class='... bg-rose-600 ... hover:bg-rose-700 ...'
```

### Impact

Low: purely cosmetic inconsistency. No functional impact.

---

## B-03

**Title:** Status badge colors differ from design system naming convention

**Severity:** Low
**Component:** `templates/contents/content_list.html`, `templates/contents/content_detail.html`
**Status:** Deferred — no functional impact

### Description

The QA report flagged that status badges use `blue`/`yellow`/`green` Tailwind color prefixes while the PRD design system referenced `sky`/`amber`/`emerald`. Both color sets are valid Tailwind palettes and produce similar visual output. The colors match the Sprint 1 design specification and are visually consistent.

### Decision

Deferred: the current palette (`blue-500`, `yellow-500`, `green-500`) matches the explicitly defined STATUS badge colors in the task specifications. No change required.

---

## Fix Summary

| ID | Files modified | Change | Migration needed |
|----|---------------|--------|-----------------|
| B-01 | `contents/views.py` | Changed `request.GET.get('q', '')` to `request.GET.get('search', '')` | No |
| B-02 | `templates/contents/content_confirm_delete.html` | Changed `red-600` to `rose-600` on delete button | No |
| B-03 | No change — deferred | — | — |
