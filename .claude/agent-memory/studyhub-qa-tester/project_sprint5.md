---
name: Sprint 5 QA findings
description: Sprint 5 AI Insights QA results — 1 FAIL (BUG-01 Medium), 2 WARNs, 17 PASS out of 20 TCs
type: project
---

## Sprint 5 — AI Insights (2026-03-25)

Overall: 17 PASS / 1 FAIL / 2 WARN out of 20 TCs.

### BUG-01 (Medium) — GenerateInsightsView returns HTTP 200 success:True when API key is missing

`AIService.generate_insights()` catches `TypeError` (raised by empty API key) via bare `except Exception` and returns `f"Unexpected error: {e}"` — a truthy non-None string. The view only checks `if result is None` to decide 503, so the error string bypasses that check and returns HTTP 200 `{"success": true, "insights": "Unexpected error: ..."}`.

Contrast: `suggest_category()` and `generate_description()` return `None` from all except branches, so they correctly return 503 on authentication errors.

**Why:** The `generate_insights` contract returns error strings (not None) to be rendered as readable text, but the view never validates that the returned string is actually a success response.

### BUG-02 (Low) — SuggestCategoryView returns misleading "AI service unavailable" when user has no categories

`suggest_category()` returns `None` early when `user_categories=[]`, before any API call. The view maps `None → 503 "AI service unavailable"` which is semantically wrong — the actual cause is "no categories defined".

### Patterns observed
- The None-sentinel pattern for suggest/generate works cleanly; insights needs a parallel fix
- All auth gates (LoginRequiredMixin) work correctly across all 3 views
- Rate limiting (check_rate_limit) works correctly — tested unit and integration
- All 3 URL patterns resolve correctly
- Dashboard and content form both render with AI panel/buttons (HTTP 200 confirmed)
- Sidebar dashboard:home link fix was confirmed in place (no regression)
- Malformed JSON returns clean 400 (not 500)
- CSRF not exempted on any view
