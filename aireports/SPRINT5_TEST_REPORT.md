## Test Report — Sprint 5 (AI Insights)
**Date:** 2026-03-25
**Tester:** QA Agent
**Server:** Django test client (no running server required)
**Branch:** main
**Commit:** 76c080f

---

### Summary
| Total | Passed | Failed | Warnings |
|---|---|---|---|
| 20 | 17 | 1 | 2 |

---

### Test Cases

#### TC-01 — Django system check
- **Pre-condition:** Virtual environment activated
- **Steps:**
  1. Run `python manage.py check`
- **Expected:** 0 issues identified
- **Actual:** `System check identified no issues (0 silenced).`
- **Status:** PASS

---

#### TC-02 — URL resolution for all 3 insight endpoints
- **Pre-condition:** `insights` app registered in `INSTALLED_APPS` and `core/urls.py`
- **Steps:**
  1. Run `python manage.py shell -c "from django.urls import reverse; print(reverse('insights:suggest_category')); ..."`
- **Expected:** `/insights/suggest-category/`, `/insights/generate-description/`, `/insights/generate-insights/`
- **Actual:**
  ```
  /insights/suggest-category/
  /insights/generate-description/
  /insights/generate-insights/
  ```
- **Status:** PASS

---

#### TC-03 — Unauthenticated requests are rejected (302 redirect)
- **Pre-condition:** No user logged in
- **Steps:**
  1. POST to `/insights/suggest-category/` without authentication
  2. POST to `/insights/generate-description/` without authentication
  3. GET `/insights/generate-insights/` without authentication
- **Expected:** HTTP 302 redirect to `/users/login/?next=<endpoint>`
- **Actual:**
  - `suggest-category`: 302 → `/users/login/?next=/insights/suggest-category/`
  - `generate-description`: 302 → `/users/login/?next=/insights/generate-description/`
  - `generate-insights`: 302 → `/users/login/?next=/insights/generate-insights/`
- **Status:** PASS

---

#### TC-04 — SuggestCategoryView: missing API key returns graceful error
- **Pre-condition:** `ANTHROPIC_API_KEY=''`, user authenticated
- **Steps:**
  1. POST `{"title": "test article", "url": ""}` to `/insights/suggest-category/`
- **Expected:** HTTP 503, JSON `{"success": false, "error": "..."}`
- **Actual:** HTTP 503, `{"success": false, "error": "AI service unavailable"}`
- **Status:** PASS

---

#### TC-05 — GenerateDescriptionView: missing API key returns graceful error
- **Pre-condition:** `ANTHROPIC_API_KEY=''`, user authenticated
- **Steps:**
  1. POST `{"title": "test article", "url": "", "content_type": "article"}` to `/insights/generate-description/`
- **Expected:** HTTP 503, JSON `{"success": false, "error": "..."}`
- **Actual:** HTTP 503, `{"success": false, "error": "AI service unavailable"}`
- **Status:** PASS

---

#### TC-06 — GenerateInsightsView: missing API key returns graceful error
- **Pre-condition:** `ANTHROPIC_API_KEY=''`, user authenticated
- **Steps:**
  1. GET `/insights/generate-insights/`
- **Expected:** HTTP 503 (or any non-200 error status), JSON `{"success": false, "error": "..."}`
- **Actual:** HTTP 200, `{"success": true, "insights": "Unexpected error: \"Could not resolve authentication method...\"}`
- **Status:** FAIL
- **Bug Reference:** BUG-01

---

#### TC-07 — Rate limiting: check_rate_limit logic
- **Pre-condition:** None (unit test via shell)
- **Steps:**
  1. Create a fresh `SessionStore`
  2. Call `check_rate_limit(session, 'test_action', max_calls=3)` four times in a row
  3. Verify first 3 calls return `True`, 4th returns `False`
  4. Set session window to 3700 seconds ago, call again — verify window resets and returns `True`
- **Expected:** Correct call counting; expired window resets counter
- **Actual:**
  - Call 1: `True`, Call 2: `True`, Call 3: `True`, Call 4: `False` (blocked)
  - After window expiry: `True`, count reset to `1`
  - Session keys: `ai_rate_{action_key}_count` and `ai_rate_{action_key}_window`
  - Uses `time.time()` for window tracking
- **Status:** PASS

---

#### TC-08 — SuggestCategoryView: rate limit exceeded returns 429
- **Pre-condition:** User authenticated, session pre-seeded with `ai_rate_suggest_category_count=10` in current window
- **Steps:**
  1. Set session count to 10 (at limit) with current window timestamp
  2. POST `{"title": "test article", "url": ""}` to `/insights/suggest-category/`
- **Expected:** HTTP 429, JSON `{"success": false, "error": "Rate limit exceeded. ..."}`
- **Actual:** HTTP 429, `{"success": false, "error": "Rate limit exceeded. Please try again later."}`
- **Status:** PASS

---

#### TC-09 — POST views reject GET requests (405)
- **Pre-condition:** User authenticated
- **Steps:**
  1. GET `/insights/suggest-category/`
  2. GET `/insights/generate-description/`
- **Expected:** HTTP 405 Method Not Allowed
- **Actual:**
  - `suggest-category`: HTTP 405
  - `generate-description`: HTTP 405
- **Status:** PASS

---

#### TC-10 — GenerateInsightsView rejects POST
- **Pre-condition:** User authenticated
- **Steps:**
  1. POST to `/insights/generate-insights/` with JSON body `{}`
- **Expected:** HTTP 405 Method Not Allowed
- **Actual:** HTTP 405
- **Status:** PASS

---

#### TC-11 — SuggestCategoryView: empty category list handled
- **Pre-condition:** User authenticated, user has no categories in database
- **Steps:**
  1. POST `{"title": "test article", "url": ""}` to `/insights/suggest-category/`
- **Expected:** Graceful response (not a crash)
- **Actual:** HTTP 503, `{"success": false, "error": "AI service unavailable"}`
- **Note:** The response does not crash and is technically graceful. However, the error message "AI service unavailable" is semantically inaccurate — the actual reason is that the user has no categories defined, not that the AI service is down. `AIService.suggest_category()` returns `None` on empty categories list (line 42–43 in `services.py`), which the view interprets as a service error.
- **Status:** WARN

---

#### TC-12 — Static analysis: services.py
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `insights/services.py`
  2. Verify all 3 AIService methods have try/except around the API call
  3. Verify catches at least `anthropic.APIError` or equivalent
  4. Verify returns None on failure for suggest/generate, error string for insights
  5. Verify `check_rate_limit` uses `time.time()`
- **Expected:** All checks pass
- **Actual:**
  - `suggest_category`: try/except on lines 55–75, catches `anthropic.APIError`, `APIConnectionError`, `RateLimitError`, `APITimeoutError`, and bare `Exception` — returns `None` on all failures. PASS
  - `generate_description`: try/except on lines 91–107, same pattern — returns `None` on all failures. PASS
  - `generate_insights`: try/except on lines 135–151, catches named errors with error strings and bare `Exception` with `f"Unexpected error: {e}"` — returns error string not `None`. PASS by spec (spec says "returns error string for insights")
  - `check_rate_limit`: uses `time.time()` at line 16. PASS
  - **Side note:** The `generate_insights` bare `except Exception` handler catches `TypeError` (raised when `ANTHROPIC_API_KEY=''`) and returns a non-None truthy string, causing `GenerateInsightsView` to return HTTP 200 with `success: True`. See BUG-01.
- **Status:** PASS

---

#### TC-13 — Static analysis: views.py
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `insights/views.py`
  2. Verify all 3 views use `LoginRequiredMixin`
  3. Verify POST views do not define `get()` (Django dispatch handles 405)
  4. Verify `@csrf_exempt` is absent
  5. Verify JSON body is parsed inside try/except
- **Expected:** All checks pass
- **Actual:**
  - `SuggestCategoryView(LoginRequiredMixin, View)`: line 18 — PASS
  - `GenerateDescriptionView(LoginRequiredMixin, View)`: line 56 — PASS
  - `GenerateInsightsView(LoginRequiredMixin, View)`: line 93 — PASS
  - POST-only enforcement: `SuggestCategoryView` and `GenerateDescriptionView` only define `post()`, so Django returns 405 for GET via `http_method_not_allowed` — PASS
  - `GenerateInsightsView` only defines `get()`, so Django returns 405 for POST — PASS
  - No `@csrf_exempt` decorator anywhere in `views.py` — PASS
  - JSON `json.loads(request.body)` in try/except `(json.JSONDecodeError, ValueError)` in both POST views — PASS
- **Status:** PASS

---

#### TC-14 — Static analysis: content_form.html
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `templates/contents/content_form.html`
  2. Verify `#btn-suggest-category` with `data-url` attribute
  3. Verify `#btn-generate-description` with `data-url` attribute
  4. Verify JS reads CSRF token from cookie
  5. Verify loading state disables button and changes text
- **Expected:** All checks pass
- **Actual:**
  - `#btn-suggest-category` at lines 104–110 with `data-url='{% url "insights:suggest_category" %}'` — PASS
  - `#btn-generate-description` at lines 125–131 with `data-url='{% url "insights:generate_description" %}'` — PASS
  - `getCookie('csrftoken')` function at lines 193–204, used in AJAX headers at line 217 — PASS
  - `btn.disabled = true` + button HTML replaced with spinner at lines 207–209, restored in `finally` block at line 233 — PASS
- **Status:** PASS

---

#### TC-15 — Static analysis: insights_panel.html
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `templates/insights/insights_panel.html`
  2. Verify `#btn-generate-insights` with `data-url`
  3. Verify JS fetches the endpoint and renders result
  4. Verify `#insights-result`, `#insights-placeholder`, `#insights-error` elements
- **Expected:** All elements and JS logic present
- **Actual:**
  - `#btn-generate-insights` at lines 13–18 with `data-url='{% url "insights:generate_insights" %}'` — PASS
  - `fetch(url, {...})` in click handler at line 67, renders result to `#insights-result` at line 76 — PASS
  - `#insights-result` at line 21 — PASS
  - `#insights-placeholder` at line 25 — PASS
  - `#insights-error` at line 29 — PASS
- **Status:** PASS

---

#### TC-16 — Dashboard includes insights panel
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `templates/dashboard/dashboard.html`
  2. Look for `{% include 'insights/insights_panel.html' %}`
- **Expected:** Include tag present in Row 5
- **Actual:** `{% include 'insights/insights_panel.html' %}` present at line 353 inside `<section aria-label='AI Insights'>` (Row 5 comment at line 351)
- **Status:** PASS

---

#### TC-17 — Sidebar dashboard link fix
- **Pre-condition:** None (code review)
- **Steps:**
  1. Read `templates/components/sidebar.html`
  2. Verify `{% url 'dashboard:home' %}` is used (not `dashboard:index`)
- **Expected:** `dashboard:home` URL name used
- **Actual:** Line 24: `{% url 'dashboard:home' as dashboard_url %}` — PASS. No reference to `dashboard:index` anywhere in the file.
- **Status:** PASS

---

#### TC-18 — Dashboard renders with insights panel (HTTP 200)
- **Pre-condition:** Test user logged in
- **Steps:**
  1. GET `/dashboard/`
  2. Check response body contains "AI Insights" text and `insights-panel` element
- **Expected:** HTTP 200, body contains "AI Insights" and `id="insights-panel"`
- **Actual:** HTTP 200, "AI Insights" present: True, "insights-panel" id present: True
- **Status:** PASS

---

#### TC-19 — Content form renders with AI buttons (HTTP 200)
- **Pre-condition:** Test user logged in
- **Steps:**
  1. GET `/contents/create/`
  2. Check response body contains `btn-suggest-category` and `btn-generate-description`
- **Expected:** HTTP 200, both button IDs present
- **Actual:** HTTP 200, `btn-suggest-category`: True, `btn-generate-description`: True
- **Status:** PASS

---

#### TC-20 — Malformed JSON body handled gracefully
- **Pre-condition:** User authenticated
- **Steps:**
  1. POST `not-json-at-all` (as raw body) to `/insights/suggest-category/`
- **Expected:** HTTP 400, JSON `{"success": false, "error": "Invalid JSON"}` (not a 500)
- **Actual:** HTTP 400, `{"success": false, "error": "Invalid JSON"}`
- **Status:** PASS

---

### Bugs Found

#### BUG-01 — GenerateInsightsView returns HTTP 200 success:True when API key is missing
- **Severity:** Medium
- **Component:** `insights/views.py` (`GenerateInsightsView`) + `insights/services.py` (`AIService.generate_insights`)
- **Description:** When `ANTHROPIC_API_KEY` is empty or invalid, `AIService.generate_insights()` raises a `TypeError` internally (not an `anthropic.APIError`). The bare `except Exception` handler in `generate_insights()` catches this and returns the string `"Unexpected error: \"Could not resolve authentication method...\"`. Because this is a non-None truthy value, `GenerateInsightsView.get()` passes the `if result is None` check and returns `{"success": true, "insights": "Unexpected error: ..."}` with HTTP 200. The frontend JavaScript treats this as a successful response and renders the raw error message as if it were valid AI insights text.
- **Reproduction:**
  1. Set `ANTHROPIC_API_KEY=''` in the environment
  2. Log in as any authenticated user
  3. GET `/insights/generate-insights/`
  4. Observe: HTTP 200 with `{"success": true, "insights": "Unexpected error: \"Could not resolve authentication method...\""}`
  5. Expected: HTTP 503 with `{"success": false, "error": "AI service unavailable"}`
- **Expected vs Actual:**
  - Expected: HTTP 503, `{"success": false, "error": "AI service unavailable"}`
  - Actual: HTTP 200, `{"success": true, "insights": "Unexpected error: ..."}`
- **Root Cause:** `generate_insights()` returns error strings (not `None`) for all exception paths. The view only checks `if result is None` to detect failure. When `TypeError` (from empty API key) is caught by `except Exception`, the method returns a truthy error string that bypasses the `None` sentinel check. In contrast, `suggest_category()` and `generate_description()` return `None` from all exception handlers, so they correctly trigger the 503 path.
- **Fix Direction:** Either (a) make `generate_insights` return `None` for unrecoverable errors like `TypeError`/`AuthenticationError` instead of an error string, and return the error string only for expected API errors, or (b) change the view to check `result.startswith('AI service')` or use a sentinel, or (c) add explicit handling for `anthropic.AuthenticationError` (which is a subclass of `anthropic.APIError`) and return `None` from that handler.

---

#### BUG-02 — SuggestCategoryView returns misleading "AI service unavailable" when user has no categories
- **Severity:** Low
- **Component:** `insights/views.py` (`SuggestCategoryView`) + `insights/services.py` (`AIService.suggest_category`)
- **Description:** When the authenticated user has zero categories defined, `AIService.suggest_category()` returns `None` early (before making any API call) because `user_categories` is an empty list. The view interprets `None` as an AI service failure and returns HTTP 503 `{"success": false, "error": "AI service unavailable"}`. The real reason is that the user has no categories, not that the AI service is down. This incorrect error message may confuse users into thinking the AI feature is broken.
- **Reproduction:**
  1. Create a new user with no categories
  2. Log in as that user
  3. POST `{"title": "test article", "url": ""}` to `/insights/suggest-category/`
  4. Observe: HTTP 503 `{"error": "AI service unavailable"}`
  5. Expected: A more informative response, e.g., HTTP 200 `{"success": false, "error": "No categories defined. Create a category first."}` or HTTP 404/422 with a clear explanation
- **Expected vs Actual:**
  - Expected: Semantically correct error indicating no categories exist
  - Actual: HTTP 503 `"AI service unavailable"` — misleading because the AI service itself is working fine
- **Fix Direction:** In `SuggestCategoryView.post()`, check if the categories queryset is empty before calling `AIService` and return a dedicated response such as `{"success": false, "error": "No categories available. Create a category first."}` with HTTP 200 or 422.
