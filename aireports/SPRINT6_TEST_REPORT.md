## Test Report — Sprint 6 (Polish & Refinements)
**Date:** 2026-03-25
**Tester:** QA Agent
**Server:** http://127.0.0.1:8000

### Summary
| Total | Passed | Failed | Warnings |
|---|---|---|---|
| 25 | 21 | 2 | 2 |

---

### Test Cases

#### TC-01 — Django system check
- **Pre-condition:** Virtual environment activated
- **Steps:** Run `python manage.py check`
- **Expected:** 0 issues
- **Actual:** "System check identified no issues (0 silenced)."
- **Status:** PASS

---

#### TC-02 — All main pages return HTTP 200
- **Pre-condition:** Authenticated test user `qa_sprint6@studyhub.com`
- **Steps:** GET `/dashboard/`, `/contents/`, `/contents/create/`, `/categories/`, `/categories/create/`, `/tags/`, `/tags/create/`
- **Expected:** All return 200
- **Actual:** All returned 200
- **Status:** PASS

---

#### TC-03 — Empty state: dashboard (no content user)
- **Pre-condition:** Fresh user with no content (`qa_empty@studyhub.com`)
- **Steps:** GET `/dashboard/`
- **Expected:** Body contains "Welcome to StudyHub"
- **Actual:** "Welcome to StudyHub!" found in response body; `{% if stats.total_contents == 0 %}` block fires correctly
- **Status:** PASS

---

#### TC-04 — Empty state: content list
- **Pre-condition:** User with no content
- **Steps:** GET `/contents/`
- **Expected:** Body contains "No content" text
- **Actual:** "No contents yet" heading found in empty state block
- **Status:** PASS

---

#### TC-05 — Empty state: categories list
- **Pre-condition:** User with no categories
- **Steps:** GET `/categories/`
- **Expected:** Body contains "No categor" text
- **Actual:** "No categories yet" found in empty state block
- **Status:** PASS

---

#### TC-06 — Empty state: tags list
- **Pre-condition:** User with no tags
- **Steps:** GET `/tags/`
- **Expected:** Body contains "No tag" text
- **Actual:** "No tags yet" found in empty state block
- **Status:** PASS

---

#### TC-07 — Flash messages: auto-dismiss attribute
- **Pre-condition:** Read `templates/components/messages.html`
- **Steps:** Inspect template for `data-message` and setTimeout logic
- **Expected:** `data-message` attribute present; setTimeout at 5000ms with fade-out
- **Actual:**
  - Line 5: `data-message` attribute present on the `<div role='alert'>` element
  - Lines 56-62: `document.querySelectorAll('[data-message]').forEach(...)` with `setTimeout(..., 5000)` applying `opacity: 0` transition followed by `el.remove()` after 500ms
- **Status:** PASS

---

#### TC-08 — Breadcrumbs: content form (create)
- **Pre-condition:** Read `templates/contents/content_form.html`
- **Steps:** Inspect breadcrumbs nav block for "Contents" and "Create" crumbs
- **Expected:** Breadcrumb shows Contents > Create
- **Actual:** Lines 9-28 of `content_form.html` contain an inline breadcrumb nav with a link to `contents:list` labelled "Contents" and a current page label "Create" when `form.instance.pk` is falsy. The breadcrumbs component (`components/breadcrumbs.html`) is NOT used — breadcrumbs are implemented inline. Functional test confirms the edit page returns 200 with both "Edit" and "Contents" in body.
- **Status:** PASS

---

#### TC-09 — Breadcrumbs: content form (edit)
- **Pre-condition:** Existing content item
- **Steps:** GET `/contents/{pk}/edit/`; inspect for "Edit" breadcrumb and back link to content detail
- **Expected:** Breadcrumb shows Contents > {title} > Edit
- **Actual:** Lines 17-24 of `content_form.html` show `form.instance.pk` branch with a link to `contents:detail` showing `{{ form.instance.title }}` and a current page label "Edit". Functional test confirmed "Edit" in body = True and "Contents" in body = True.
- **Status:** PASS

---

#### TC-10 — Breadcrumbs: content detail
- **Pre-condition:** Existing content item
- **Steps:** Read `templates/contents/content_detail.html`; check for "Contents" breadcrumb
- **Expected:** Breadcrumb shows Contents > {title}
- **Actual:** Lines 9-18 of `content_detail.html` contain inline breadcrumb nav with link to `contents:list` labelled "Contents" and current page showing `{{ content.title }}`
- **Status:** PASS

---

#### TC-11 — Breadcrumbs: category form
- **Pre-condition:** Read `templates/categories/category_form.html`
- **Steps:** Inspect for "Categories" breadcrumb
- **Expected:** Breadcrumb shows Categories > Create/Edit
- **Actual:** Lines 10-25 contain inline breadcrumb nav with "Categories" link and "Create"/"Edit" as current page. Back link also present.
- **Status:** PASS

---

#### TC-12 — Breadcrumbs: tag form
- **Pre-condition:** Read `templates/tags/tag_form.html`
- **Steps:** Inspect for "Tags" breadcrumb
- **Expected:** Breadcrumb shows Tags > Create
- **Actual:** Lines 8-20 contain inline breadcrumb nav with "Tags" link and "Create" as current page. Back link also present.
- **Status:** PASS

---

#### TC-13 — Breadcrumbs component file exists
- **Pre-condition:** Check `templates/components/breadcrumbs.html`
- **Steps:** Verify file exists and has correct structure
- **Expected:** File exists with `{% if breadcrumbs %}` block and `{% for crumb in breadcrumbs %}` loop
- **Actual:** File exists at `templates/components/breadcrumbs.html`. Structure is correct: `{% if breadcrumbs %}`, `{% for crumb in breadcrumbs %}`, `{% if not forloop.last %}` for link vs current-page rendering. However, none of the form or detail templates actually use `{% include 'components/breadcrumbs.html' %}` — they all implement breadcrumbs inline. The component is unused.
- **Status:** WARN — Component file exists and is correctly structured, but is never included by any page template. This means the component is dead code. All breadcrumbs are hardcoded inline per-template. Functionally the breadcrumbs work, but the reusable component pattern is not being leveraged.

---

#### TC-14 — Mobile sidebar HTML structure
- **Pre-condition:** Read `templates/base.html`
- **Steps:** Inspect for hamburger button, overlay, backdrop, and JS toggle functions
- **Expected:** Hamburger with `md:hidden`, overlay with `md:hidden`, backdrop element, JS toggle
- **Actual:**
  - Lines 56-67: Hamburger button container with `md:hidden` class, `onclick='openMobileSidebar()'`, and SVG hamburger icon
  - Lines 34-38: `#mobile-sidebar-overlay` div with `hidden md:hidden` and `onclick='closeMobileSidebar()'`
  - Lines 41-45: `#mobile-sidebar` drawer with `-translate-x-full md:hidden transition-transform`
  - Lines 80-108: `openMobileSidebar()`, `closeMobileSidebar()`, and DOMContentLoaded listener to auto-close on nav link click
- **Status:** PASS

---

#### TC-15 — URL auto-detect JS in content form
- **Pre-condition:** Read `templates/contents/content_form.html`
- **Steps:** Inspect for blur event on `#id_url`, YouTube regex, and default-only condition
- **Expected:** `blur` event listener, YouTube regex present, fires only when content_type is at default
- **Actual:**
  - Line 306: `urlInput.addEventListener('blur', function() {...})` present
  - Line 299: `{ regex: /youtube\.com|youtu\.be/i, type: 'video' }` present along with patterns for spotify, instagram/twitter, amazon/goodreads, udemy/coursera/edX
  - Lines 310-311: Guard condition `if (currentVal && currentVal !== typeSelect.options[0].value) return;` — only auto-sets if user hasn't selected a type
- **Status:** PASS

---

#### TC-16 — Tag picker JS in content form
- **Pre-condition:** Read `templates/contents/content_form.html`
- **Steps:** Verify hidden select or existing select hidden with JS pill sync
- **Expected:** Hidden `<select>` for tags or existing select hidden; tag pill elements; JS syncs hidden select with pill state
- **Actual:** The implementation uses Django's built-in `CheckboxSelectMultiple` widget rendered as `{% for checkbox in form.tags %}`. Each checkbox is a real `<input type="checkbox">` inside a `<label>` styled with `group-has-[:checked]` CSS-only toggling for the pill visual. There is no hidden select element and no JavaScript syncing of state. The checkboxes ARE the form field — clicking them natively submits the correct tags. No JS pill toggle is implemented.
- **Status:** WARN — Functionally correct (tags submit properly via native checkboxes), but the sprint spec explicitly calls for "Hidden select for tags" and "JS syncs hidden select with pill state." The CSS-driven checkbox-as-pill approach is a valid alternative that works, but deviates from the described implementation. The `form.tags` field checkbox behaviour is not what a JS tag-picker implies.

---

#### TC-17 — Client-side validation in content form
- **Pre-condition:** Read `templates/contents/content_form.html`
- **Steps:** Check for `novalidate` on form, submit event listener, required field checks, and error CSS class
- **Expected:** `novalidate` on `<form>`; submit event listener checking required fields; error CSS class added on invalid
- **Actual:**
  - Line 48: `<form method='POST' novalidate>` — `novalidate` is present
  - The JavaScript block (lines 213-334) contains AI button handlers and URL auto-detect logic ONLY. There is NO submit event listener that validates required fields. There is NO error CSS class applied to fields on invalid input. With `novalidate` present, browser validation is disabled, and no custom JS validation replaces it. Server-side validation still works, but client-side form validation (as specified in 6.5) is absent.
- **Status:** FAIL — `novalidate` is set but client-side submit validation is not implemented. Required field checking and error state CSS classes on invalid submission are missing.

---

#### TC-18 — Back links exist on form/detail pages
- **Pre-condition:** Read content_detail.html, content_form.html, category_form.html, tag_form.html
- **Steps:** Check each template for a back link element
- **Expected:** Each page contains a back link (arrow or "Back" text)
- **Actual:**
  - `content_detail.html` lines 22-28: "Back to Contents" link with left-arrow SVG
  - `content_form.html` lines 32-38: "Back to Contents" link with left-arrow SVG
  - `category_form.html` lines 28-34: "Back to Categories" link with left-arrow SVG
  - `tag_form.html` lines 22-28: "Back to Tags" link with left-arrow SVG
- **Status:** PASS

---

#### TC-19 — Sidebar active state correctness
- **Pre-condition:** Read `templates/components/sidebar.html`
- **Steps:** Check URL name for dashboard, slice lengths for each nav section
- **Expected:** `dashboard:home` used; `/contents` slice = 9, `/categories` slice = 11, `/tags` slice = 5, `/insights` slice = 9
- **Actual:**
  - Line 24: `{% url 'dashboard:home' as dashboard_url %}` — correct
  - Line 44: `request.path|slice:":9" == "/contents"` — `/contents` is 9 chars, correct
  - Line 62: `request.path|slice:":11" == "/categories"` — `/categories` is 11 chars, correct
  - Line 76: `request.path|slice:":5" == "/tags"` — `/tags` is 5 chars, correct
  - Line 91: `request.path|slice:":9" == "/insights"` — `/insights` is 9 chars, correct
- **Status:** PASS

---

#### TC-20 — Dashboard welcome onboarding section
- **Pre-condition:** Read `templates/dashboard/dashboard.html`
- **Steps:** Verify `{% if stats.total_contents == 0 %}` block with welcome heading and 3 action cards
- **Expected:** Condition present; welcome heading; 3 quick-start cards (Add Content, Create a Category, Create a Tag)
- **Actual:**
  - Line 19: `{% if stats.total_contents == 0 %}` present
  - Line 29: `<h2 class='...'>Welcome to StudyHub!</h2>` present
  - Lines 36-52: "Add Content" card linking to `contents:create`
  - Lines 55-68: "Create a Category" card linking to `categories:create`
  - Lines 71-85: "Create a Tag" card linking to `tags:create`
  - Line 90: `{% endif %}` closes block
- **Status:** PASS

---

#### TC-21 — CRUD messages: all apps fire messages
- **Pre-condition:** Read `contents/views.py`, `categories/views.py`, `tags/views.py`
- **Steps:** Verify `messages.success(...)` in form_valid/delete_view for all operations
- **Expected:** All create, update, delete operations call messages.success
- **Actual:**
  - `contents/views.py`: Create (line 89), Update (line 110), Delete (line 126), StatusUpdate (line 138) — all present
  - `categories/views.py`: Create (line 30), Update (line 46), Delete (line 62) — all present
  - `tags/views.py`: Create (line 30), Delete (line 46) — all present (tags has no update view)
- **Status:** PASS

---

#### TC-22 — Content create/edit/delete flow (functional)
- **Pre-condition:** Authenticated test user
- **Steps:** POST create, update, delete with valid data
- **Expected:** All three POST requests return 302
- **Actual:** All three returned 302. Detail page GET returned 200.
- **Status:** PASS

---

#### TC-23 — Category create/delete flow (functional)
- **Pre-condition:** Authenticated test user
- **Steps:** POST create and delete category
- **Expected:** Both return 302
- **Actual:** POST `/categories/create/` → 302; POST `/categories/{pk}/delete/` → 302
- **Status:** PASS

---

#### TC-24 — Tag create/delete flow (functional)
- **Pre-condition:** Authenticated test user
- **Steps:** POST create and delete tag
- **Expected:** Both return 302
- **Actual:** POST `/tags/create/` → 302; POST `/tags/{pk}/delete/` → 302
- **Status:** PASS

---

#### TC-25 — No broken template tags
- **Pre-condition:** Authenticated test user
- **Steps:** GET all main pages and `/insights/`
- **Expected:** All return 200 (no TemplateSyntaxError → 500)
- **Actual:** All 8 pages returned 200: `/dashboard/`, `/contents/`, `/contents/create/`, `/categories/`, `/categories/create/`, `/tags/`, `/tags/create/`, `/insights/`
- **Status:** PASS

---

### Bugs Found

#### BUG-01 — Client-side form validation not implemented in content form
- **Severity:** Medium
- **Component:** `templates/contents/content_form.html`
- **Description:** Sprint 6.5 specifies client-side form validation: a submit event listener checking required fields and applying error state CSS classes when fields are invalid. The `<form>` has `novalidate` which disables browser-native validation, but the replacement JS validation is absent. Users submitting with an empty Title field receive no immediate client-side feedback — only a full-page reload with server-side errors.
- **Reproduction:**
  1. Log in and navigate to `/contents/create/`
  2. Leave the Title field blank
  3. Click "Save Content"
  4. Observe: the form submits to the server and returns a full page with a server-side validation error. No client-side error indicator appears before submission.
- **Expected vs Actual:** Expected a submit event listener to intercept the submission, highlight the empty Title field with an error CSS class, and prevent the POST. Actual: no client-side intercept occurs; form posts directly to server.

---

#### BUG-02 — Status badge colors deviate from design system in content_list and content_detail (regression from Sprint 4)
- **Severity:** Medium
- **Component:** `templates/contents/content_list.html`, `templates/contents/content_detail.html`
- **Description:** The design system specifies status badge colors as: New = `sky`, In Progress = `amber`, Completed = `emerald`. Both content_list.html and content_detail.html use `blue`, `yellow`, and `green` instead. The quick-status action buttons in content_detail.html also use `blue`, `yellow`, `green`. This was flagged in the Sprint 4 report and remains unfixed. The dashboard (`dashboard.html`) correctly uses `sky`/`amber`/`emerald` for the stat cards.
- **Reproduction:**
  1. Create a content item with status "New"
  2. View the content list at `/contents/`
  3. Inspect the "New" badge — it uses `bg-blue-500/10 text-blue-400` instead of `bg-sky-500/10 text-sky-400`
  4. Repeat for "In Progress" (yellow vs amber) and "Completed" (green vs emerald)
  5. Same discrepancy in content detail view at `/contents/{pk}/`
- **Expected vs Actual:**
  - New badge: `bg-sky-500/10 text-sky-400 border-sky-500/20` — Actual: `bg-blue-500/10 text-blue-400 border-blue-500/20`
  - In Progress badge: `bg-amber-500/10 text-amber-400 border-amber-500/20` — Actual: `bg-yellow-500/10 text-yellow-400 border-yellow-500/20`
  - Completed badge: `bg-emerald-500/10 text-emerald-400 border-emerald-500/20` — Actual: `bg-green-500/10 text-green-400 border-green-500/20`
- **Affected files:**
  - `/Users/mindera/github/studyhub/templates/contents/content_list.html` lines 176-188, 277-316, 349-355
  - `/Users/mindera/github/studyhub/templates/contents/content_detail.html` lines 55-59, 163-196

---

### Warnings (non-blocking)

#### WARN-01 — Breadcrumbs component file exists but is never used
- **Component:** `templates/components/breadcrumbs.html`
- **Description:** A reusable breadcrumbs component was created at `templates/components/breadcrumbs.html` with the correct `{% if breadcrumbs %}` / `{% for crumb in breadcrumbs %}` pattern. However, none of the form or detail templates use `{% include 'components/breadcrumbs.html' %}` — all breadcrumbs are hardcoded inline per template. The component is functional dead code. No user-visible impact, but the DRY intention of the component is not realized.

---

#### WARN-02 — Tag picker uses CSS-driven checkboxes, not JS pill picker as specified
- **Component:** `templates/contents/content_form.html`
- **Description:** Sprint 6.5 specifies a JS tag picker with a hidden select and JavaScript syncing pill state. The implementation instead uses Django's `CheckboxSelectMultiple` widget with `group-has-[:checked]` Tailwind CSS classes for the visual pill effect. The native checkboxes are hidden via the `{{ checkbox.tag }}` label wrapper. Functionally, tags are selected and submitted correctly. The discrepancy is in approach, not in outcome.

---

### Design System Compliance Summary

| Element | Expected | Content List | Content Detail | Dashboard |
|---|---|---|---|---|
| New badge | `sky` | `blue` (FAIL) | `blue` (FAIL) | `sky` (PASS) |
| In Progress badge | `amber` | `yellow` (FAIL) | `yellow` (FAIL) | `amber` (PASS) |
| Completed badge | `emerald` | `green` (FAIL) | `green` (FAIL) | `emerald` (PASS) |
| Page background | `gray-950` | N/A (base.html) | PASS | PASS |
| Card background | `gray-900` | PASS | PASS | PASS |
| Primary button | gradient violet-indigo | PASS | PASS | PASS |
| Sidebar active | `violet-600/10 text-violet-400` | PASS | PASS | PASS |
