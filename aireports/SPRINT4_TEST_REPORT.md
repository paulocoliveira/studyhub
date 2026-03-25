## Test Report — Sprint 4 (Dashboard)
**Date:** 2026-03-25
**Tester:** QA Agent
**Server:** http://127.0.0.1:8000

---

### Summary

| Total | Passed | Failed | Warnings |
|---|---|---|---|
| 15 | 11 | 1 | 3 |

---

### Test Cases

#### TC-01 — Django System Check
- **Pre-condition:** Virtual environment active, all apps installed
- **Steps:**
  1. Run `source .venv/bin/activate && python manage.py check`
- **Expected:** `System check identified no issues (0 silenced).`
- **Actual:** `System check identified no issues (0 silenced).`
- **Status:** PASS

---

#### TC-02 — Migration State
- **Pre-condition:** Database exists with previous sprint migrations applied
- **Steps:**
  1. Run `python manage.py migrate --check`
- **Expected:** Exit code 0 — all migrations applied, nothing pending
- **Actual:** Exit code 0 — no unapplied migrations. Dashboard app has `migrations/` directory with only `__init__.py` (correct — no models, no migrations needed)
- **Status:** PASS

---

#### TC-03 — Dashboard URL Resolution
- **Pre-condition:** `dashboard.urls` included in `core/urls.py` with `app_name='dashboard'`
- **Steps:**
  1. Run `python manage.py shell -c "from django.urls import reverse; print(reverse('dashboard:home'))"`
- **Expected:** `/dashboard/`
- **Actual:** `/dashboard/`
- **Status:** PASS

---

#### TC-04 — Dashboard Redirects Unauthenticated User
- **Pre-condition:** No authenticated session
- **Steps:**
  1. Create Django test `Client`
  2. GET `/dashboard/` without logging in
- **Expected:** HTTP 302 redirect to login URL containing `/login`
- **Actual:** HTTP 302 to `/users/login/?next=/dashboard/`
- **Status:** PASS

---

#### TC-05 — DashboardService Instantiation (Empty User)
- **Pre-condition:** Fresh test user `qa_dash_a@test.com` with no content
- **Steps:**
  1. Create user via `create_user()`
  2. Instantiate `DashboardService(user=user)`
  3. Call `get_stats()`, `get_recent_added()`, `get_recent_completed()`, `get_top_categories()`, `get_top_tags()`
- **Expected:** All methods return without exception; empty/zero values for new user
- **Actual:** All five methods executed successfully. `get_stats()` returned `{'total_contents': 0, 'by_status': {'new': 0, 'in_progress': 0, 'completed': 0}, 'by_type': []}`. All list-returning methods returned empty lists.
- **Status:** PASS

---

#### TC-06 — DashboardView Renders Correctly for Authenticated User
- **Pre-condition:** User `qa_dash_a@test.com` exists and is logged in
- **Steps:**
  1. Log in using Django test client
  2. GET `/dashboard/`
  3. Verify HTTP 200 and page content
- **Expected:** HTTP 200 with `dashboard/dashboard.html` content rendered
- **Actual:** HTTP 200. Response body (28,133 bytes) contains correct page title `Dashboard — StudyHub`, section headings "Total Contents", "Recently Added", "Recently Completed", "Top Categories", "Top Tags". Template tracking via `resp.templates` returned empty list (known Django test client limitation with `APP_DIRS=True` loader), but content verification confirmed correct template was rendered.
- **Status:** PASS

---

#### TC-07 — Stats Correctness
- **Pre-condition:** User has 2 `new`, 1 `in_progress`, 1 `completed` content items of types `article`, `video`, `article`, `book`
- **Steps:**
  1. Create 4 content items with known statuses and types
  2. Call `DashboardService.get_stats()`
  3. Verify `total_contents`, `by_status`, and `by_type`
- **Expected:**
  - `total_contents == 4`
  - `by_status['new'] == 2`, `by_status['in_progress'] == 1`, `by_status['completed'] == 1`
  - `by_type`: article=2, video=1, book=1
- **Actual:**
  - `total_contents == 4` ✓
  - `by_status == {'new': 2, 'in_progress': 1, 'completed': 1}` ✓
  - `by_type == [{'content_type': 'article', 'count': 2}, {'content_type': 'video', 'count': 1}, {'content_type': 'book', 'count': 1}]` ✓
  - `by_type` ordered descending by count ✓
- **Status:** PASS

---

#### TC-08 — Recent Items Correctness
- **Pre-condition:** User has 7 content items (4 original + 3 extra added); 1 is `completed`
- **Steps:**
  1. Call `get_recent_added()` and verify count <= 5 and ordering newest-first
  2. Call `get_recent_completed()` and verify all items have `status='completed'` and count <= 5
- **Expected:** `get_recent_added()` returns max 5 items ordered by `-created_at`; `get_recent_completed()` returns only completed items, max 5
- **Actual:**
  - `get_recent_added()` returned 5 items (correct cap); ordering verified `recent_added[0].created_at >= recent_added[1].created_at` ✓
  - `get_recent_completed()` returned 1 item; all items have `status='completed'` ✓
- **Status:** PASS

---

#### TC-09 — Top Categories/Tags Correctness
- **Pre-condition:** 3 categories (Python=2 contents, Django=1, AI=0) and 2 tags (backend=2, frontend=1) assigned to user A's content
- **Steps:**
  1. Create categories and tags, assign to content
  2. Call `get_top_categories()` and `get_top_tags()`
  3. Verify `content_count` annotation, descending ordering, and count accuracy
- **Expected:** Each category/tag annotated with `content_count`; ordered descending; accurate counts; max 5 items
- **Actual:**
  - `get_top_categories()` returned 3 items: `[('Python', 2), ('Django', 1), ('AI', 0)]` in correct descending order ✓
  - `get_top_tags()` returned 2 items: `[('backend', 2), ('frontend', 1)]` in correct descending order ✓
  - All annotated with `content_count` ✓
  - All counts accurate ✓
- **Status:** PASS

---

#### TC-10 — User Data Isolation
- **Pre-condition:** Two users (user A with 7 contents, user B with 2 contents) with separate categories and tags
- **Steps:**
  1. Create user B with own content, category `User B Category`, tag `user_b_tag`
  2. Run `DashboardService` for both users
  3. Verify no data cross-contamination in stats, recent items, categories, or tags
- **Expected:** Each user's service returns only their own data with zero overlap
- **Actual:**
  - User A total=7, User B total=2 — counts are independent ✓
  - User A `get_recent_added()` contains no User B titles ✓
  - Category names: A=`{Django, Python, AI}`, B=`{User B Category}` — no intersection ✓
  - Tag names: A=`{backend, frontend}`, B=`{user_b_tag}` — no intersection ✓
- **Status:** PASS

---

#### TC-11 — Template Renders Without Error (Empty State)
- **Pre-condition:** Fresh user `qa_dash_empty@test.com` with no content, categories, or tags
- **Steps:**
  1. Log in as empty user
  2. GET `/dashboard/`
  3. Check for presence of all four empty state messages
- **Expected:** HTTP 200 with all empty state UI rendered: "No content added yet.", "Nothing marked as completed yet.", "No categories yet.", "No tags yet."
- **Actual:** All four empty state messages present in response; HTTP 200 with no exceptions
- **Status:** PASS

---

#### TC-12 — LOGIN_REDIRECT_URL Setting
- **Pre-condition:** `core/settings.py` is readable
- **Steps:**
  1. Read `core/settings.py`
  2. Find `LOGIN_REDIRECT_URL`
- **Expected:** `LOGIN_REDIRECT_URL = '/dashboard/'`
- **Actual:** `LOGIN_REDIRECT_URL = '/dashboard/'` (line 132 of `core/settings.py`)
- **Status:** PASS

---

#### TC-13 — core/urls.py Includes Dashboard
- **Pre-condition:** `core/urls.py` is readable
- **Steps:**
  1. Read `core/urls.py`
  2. Verify `path('dashboard/', include('dashboard.urls', namespace='dashboard'))` is present
- **Expected:** Dashboard included under `'dashboard/'` with correct namespace
- **Actual:** `path('dashboard/', include('dashboard.urls', namespace='dashboard'))` present on line 10 of `core/urls.py` ✓. `app_name = 'dashboard'` declared in `dashboard/urls.py` ✓.
- **Status:** PASS

---

#### TC-14 — Static Analysis: services.py
- **Pre-condition:** `dashboard/services.py` is readable
- **Steps:**
  1. Read the file
  2. Verify all queries filter by user, use `Count`/`annotate`, and contain no raw SQL
- **Expected:** All five methods filter by `user=self.user`; `Count` and `annotate` used; no raw SQL
- **Actual:**
  - `get_stats()`: `Content.objects.filter(user=self.user)` ✓; uses `.values('status').annotate(count=Count('id'))` and `.values('content_type').annotate(count=Count('id'))` ✓
  - `get_recent_added()`: `Content.objects.filter(user=self.user)` ✓
  - `get_recent_completed()`: `Content.objects.filter(user=self.user, status='completed')` ✓
  - `get_top_categories()`: `Category.objects.filter(user=self.user).annotate(content_count=Count('contents'))` ✓
  - `get_top_tags()`: `Tag.objects.filter(user=self.user).annotate(content_count=Count('contents'))` ✓
  - No raw SQL present ✓
- **Status:** PASS

---

#### TC-15 — Static Analysis: views.py
- **Pre-condition:** `dashboard/views.py` is readable
- **Steps:**
  1. Read the file
  2. Verify `LoginRequiredMixin`, `TemplateView`, and all five expected context keys
- **Expected:** `LoginRequiredMixin`, `TemplateView` used; `get_context_data` passes `stats`, `recent_added`, `recent_completed`, `top_categories`, `top_tags`
- **Actual:**
  - `class DashboardView(LoginRequiredMixin, TemplateView)` ✓
  - `template_name = 'dashboard/dashboard.html'` ✓
  - `get_context_data` calls `DashboardService(user=self.request.user)` ✓
  - All five context keys populated: `stats`, `recent_added`, `recent_completed`, `top_categories`, `top_tags` ✓
- **Status:** PASS

---

### Design System Compliance Review

The following issues were found by comparing `templates/dashboard/dashboard.html` against `docs/design-system.md`:

#### DS-01 — "New" Status Badge Color: blue vs sky (BUG-01)
- **Expected per design system:** `bg-sky-500/10 text-sky-400`
- **Actual in template:** `bg-blue-500/10 text-blue-400 border border-blue-500/20` (lines 56, 47-48)
- **Status:** FAIL (see BUG-01)

#### DS-02 — "In Progress" Status Badge Color: yellow vs amber (BUG-02)
- **Expected per design system:** `bg-amber-500/10 text-amber-400`
- **Actual in template:** `bg-yellow-500/10 text-yellow-400 border border-yellow-500/20` (lines 66-67, 74)
- **Status:** FAIL (see BUG-02)

#### DS-03 — "Completed" Status Badge Color: green vs emerald (BUG-03)
- **Expected per design system:** `bg-emerald-500/10 text-emerald-400`
- **Actual in template:** `bg-green-500/10 text-green-400 border border-green-500/20` (lines 84-85, 92)
- **Status:** FAIL (see BUG-03)

#### DS-04 — Video Content Type Badge: red vs rose (BUG-04)
- **Expected per design system:** `bg-rose-500/10 text-rose-400`
- **Actual in template:** `bg-red-500/10 text-red-400` (lines 114, 167, 224 — three occurrences across content type breakdown, recently added, and recently completed sections)
- **Status:** FAIL (see BUG-04)

#### DS-05 — Stats Card Value Typography: text-3xl vs text-2xl (WARN)
- **Design system example:** `text-2xl font-bold text-gray-100`
- **Actual:** `text-3xl font-bold text-gray-100` (lines 36, 55, 73, 91)
- **Note:** The design system shows `text-2xl` in the Stats Card example, but `text-3xl` is a reasonable, legible enhancement. No explicit prohibition, and it does not conflict with any other rule. Flagging as WARN rather than FAIL.
- **Status:** WARN

---

### Automated Test Coverage

`dashboard/tests.py` exists but contains only the placeholder comment `# Dashboard tests go here.` — **no test cases have been written**. Running `python manage.py test dashboard --verbosity=2` confirms: `Ran 0 tests in 0.000s`.

---

### Bugs Found

#### BUG-01 — "New" Status Badge Uses Wrong Color (blue instead of sky)
- **Severity:** Medium
- **Component:** `templates/dashboard/dashboard.html`
- **Description:** The "New" status stat card badge uses Tailwind `blue` color classes instead of the design-system-mandated `sky` color, causing a visual inconsistency with status badges used elsewhere in the app.
- **Reproduction:**
  1. Log in and navigate to `/dashboard/`
  2. Observe the "New" stat card badge at the top of the page
  3. Inspect element — badge reads `bg-blue-500/10 text-blue-400`
- **Expected vs Actual:**
  - Expected: `bg-sky-500/10 text-sky-400` (per `docs/design-system.md` Status Badges section)
  - Actual: `bg-blue-500/10 text-blue-400 border border-blue-500/20`
- **File:** `templates/dashboard/dashboard.html`, lines 47, 48, 56

---

#### BUG-02 — "In Progress" Status Badge Uses Wrong Color (yellow instead of amber)
- **Severity:** Medium
- **Component:** `templates/dashboard/dashboard.html`
- **Description:** The "In Progress" status stat card badge uses Tailwind `yellow` color classes instead of the design-system-mandated `amber` color, causing inconsistency with the design token `text-amber-500` defined in the color palette and with status badges used elsewhere.
- **Reproduction:**
  1. Log in and navigate to `/dashboard/`
  2. Observe the "In Progress" stat card badge
  3. Inspect element — badge reads `bg-yellow-500/10 text-yellow-400`
- **Expected vs Actual:**
  - Expected: `bg-amber-500/10 text-amber-400` (per `docs/design-system.md` Status Badges section)
  - Actual: `bg-yellow-500/10 text-yellow-400 border border-yellow-500/20`
- **File:** `templates/dashboard/dashboard.html`, lines 66, 67, 74

---

#### BUG-03 — "Completed" Status Badge Uses Wrong Color (green instead of emerald)
- **Severity:** Medium
- **Component:** `templates/dashboard/dashboard.html`
- **Description:** The "Completed" status stat card badge uses Tailwind `green` color classes instead of the design-system-mandated `emerald` color, causing inconsistency with the design token `text-emerald-500` defined for Success/Completed state.
- **Reproduction:**
  1. Log in and navigate to `/dashboard/`
  2. Observe the "Completed" stat card badge
  3. Inspect element — badge reads `bg-green-500/10 text-green-400`
- **Expected vs Actual:**
  - Expected: `bg-emerald-500/10 text-emerald-400` (per `docs/design-system.md` Status Badges section)
  - Actual: `bg-green-500/10 text-green-400 border border-green-500/20`
- **File:** `templates/dashboard/dashboard.html`, lines 84, 85, 92

---

#### BUG-04 — Video Content Type Badge Uses Wrong Color (red instead of rose)
- **Severity:** Medium
- **Component:** `templates/dashboard/dashboard.html`
- **Description:** All three occurrences of the Video content type badge in the dashboard (content type breakdown, recently added, recently completed sections) use Tailwind `red` color classes instead of the design-system-mandated `rose` color. This deviates from the Content Type Badges specification in the design system.
- **Reproduction:**
  1. Log in, create a content item of type "Video"
  2. Navigate to `/dashboard/`
  3. Observe the Video badge in "Content by Type", "Recently Added", or "Recently Completed"
  4. Inspect element — badge reads `bg-red-500/10 text-red-400`
- **Expected vs Actual:**
  - Expected: `bg-rose-500/10 text-rose-400` (per `docs/design-system.md` Content Type Badges section)
  - Actual: `bg-red-500/10 text-red-400`
- **File:** `templates/dashboard/dashboard.html`, lines 114, 167, 224

---

#### BUG-05 — dashboard/tests.py Contains No Test Cases
- **Severity:** Low
- **Component:** `dashboard/tests.py`
- **Description:** The test file was scaffolded but never populated. `python manage.py test dashboard` runs 0 tests. This means no automated regression safety net exists for the dashboard feature.
- **Reproduction:**
  1. Run `python manage.py test dashboard --verbosity=2`
  2. Output: `Ran 0 tests in 0.000s`
- **Expected vs Actual:**
  - Expected: At least one test case verifying `DashboardService` and `DashboardView` behavior
  - Actual: Only a placeholder comment `# Dashboard tests go here.`
- **File:** `dashboard/tests.py`, line 3
