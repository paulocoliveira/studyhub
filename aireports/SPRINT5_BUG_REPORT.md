# Sprint 5 — Bug Report
## StudyHub — AI Insights

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite · anthropic SDK
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 2
**Fixed:** 2 (during QA)
**Pending:** 0

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Medium | `insights/services.py` · `insights/views.py` | Fixed |
| [B-02](#b-02) | Low | `insights/views.py` | Fixed |

---

## B-01

**Title:** `GenerateInsightsView` returns HTTP 200 `success: true` when API key is missing

**Severity:** Medium
**Component:** `insights/services.py` — `AIService.generate_insights()` · `insights/views.py` — `GenerateInsightsView`
**Status:** Fixed
**Discovered in:** TC-06 (graceful error handling with empty API key)
**Fix date:** 2026-03-25

### Description

When `ANTHROPIC_API_KEY` is empty (or invalid), calling `GenerateInsightsView` returned `{"success": true, "insights": "Unexpected error: ..."}` with HTTP 200 instead of a proper error response. The frontend would then render the raw internal error string as if it were valid AI output, confusing the user.

The two other AI views (`SuggestCategoryView`, `GenerateDescriptionView`) behaved correctly, returning HTTP 503 on failure.

### Steps to reproduce

1. Ensure `ANTHROPIC_API_KEY` is not set in the environment
2. Log in and GET `/insights/generate-insights/`
3. Observe: `{"success": true, "insights": "Unexpected error: ..."}`

### Expected behavior

```json
{"success": false, "error": "AI service unavailable. Please try again later."}
```
with HTTP 503.

### Actual behavior

```json
{"success": true, "insights": "Unexpected error: ..."}
```
with HTTP 200.

### Root cause

`AIService.generate_insights()` returned error strings (not `None`) from all its `except` branches, for example:

```python
except Exception as e:
    return f'Unexpected error: {e}'   # truthy string, not None
```

`GenerateInsightsView` used `if result is None` as its sole failure sentinel. A truthy error string bypassed the 503 branch and was returned as a successful AI result. This differed from `suggest_category()` and `generate_description()`, which correctly returned `None` on all failure paths.

### Fix applied

**`insights/services.py`** — All exception handlers in `generate_insights()` now return `None`:

```python
# Before
except Exception as e:
    return f'Unexpected error: {e}'

# After
except Exception:
    return None
```

**`insights/views.py`** — `GenerateInsightsView` now returns 503 when `result is None`:

```python
if result is None:
    return JsonResponse(
        {'success': False, 'error': 'AI service unavailable. Please try again later.'},
        status=503
    )
```

### Impact

Without the fix, internal error messages (potentially including stack trace fragments) were surfaced to the user as AI-generated insights. Any API authentication failure silently appeared as a successful response.

---

## B-02

**Title:** `SuggestCategoryView` returns misleading "AI service unavailable" when user has no categories

**Severity:** Low
**Component:** `insights/views.py` — `SuggestCategoryView`
**Status:** Fixed
**Discovered in:** TC-11 (empty category list edge case)
**Fix date:** 2026-03-25

### Description

When a user has no categories, `SuggestCategoryView` returned HTTP 503 with `"error": "AI service unavailable"`. The real reason was that the user had not created any categories yet — no API call was ever made. This confusing error message could lead users to believe the AI service was down when it was actually fully operational.

### Steps to reproduce

1. Log in as a user with no categories
2. Go to `/contents/create/`
3. Click "✨ AI Suggest"
4. Observe: error message "AI service unavailable" with HTTP 503

### Expected behavior

HTTP 400 with a clear, actionable message: `"Create at least one category before using AI suggestions."`

### Actual behavior

HTTP 503: `"AI service unavailable"` — identical to a real API failure, even though no API call was attempted.

### Root cause

`AIService.suggest_category()` returns `None` early when the category list is empty (before making any API call). The view mapped all `None` results uniformly to `{"success": false, "error": "AI service unavailable"}` with status 503, with no distinction between "no categories" and "API failure".

```python
# Before — no early check in the view
categories = Category.objects.filter(user=request.user).values_list('name', flat=True)
result = AIService().suggest_category(title, url, list(categories))
if result is None:
    return JsonResponse({'success': False, 'error': 'AI service unavailable'}, status=503)
```

### Fix applied

**`insights/views.py`** — Added an early guard in `SuggestCategoryView` before the rate limit check:

```python
category_names = list(Category.objects.filter(user=request.user).values_list('name', flat=True))
if not category_names:
    return JsonResponse(
        {'success': False, 'error': 'Create at least one category before using AI suggestions.'},
        status=400
    )
```

This fires before the rate limit counter is incremented, so the user's quota is not consumed for a request that required no API call.

### Impact

Low impact — no data loss or security risk. However, a misleading "service unavailable" message on a working system damages trust in the AI feature and may cause users to file false bug reports.

---

## Fix Summary

| ID | Modified file | Change | Migration needed |
|----|--------------|--------|-----------------|
| B-01 | `insights/services.py` | All `except` branches in `generate_insights()` return `None` instead of error strings | No |
| B-01 | `insights/views.py` | `GenerateInsightsView` maps `None` result to HTTP 503 | No |
| B-02 | `insights/views.py` | `SuggestCategoryView` returns HTTP 400 with clear message when category list is empty | No |
