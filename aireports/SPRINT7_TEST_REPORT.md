## Test Report — Sprint 7 (Content Cards, Link Previews & File Upload)
**Date:** 2026-03-25
**Tester:** QA Agent
**Server:** Static/shell tests only (dev server not required for this sprint's scope)

### Summary
| Total | Passed | Failed | Warnings |
|---|---|---|---|
| 25 | 22 | 2 | 1 |

---

### Test Cases

#### TC-01 — Django system check
- **Pre-condition:** Virtual environment activated
- **Steps:** Run `python manage.py check`
- **Expected:** "System check identified no issues (0 silenced)."
- **Actual:** System check identified no issues (0 silenced).
- **Status:** PASS

#### TC-02 — Migrations applied
- **Pre-condition:** Virtual environment activated
- **Steps:** Run `python manage.py migrate --check`
- **Expected:** Exit 0, no unapplied migrations
- **Actual:** Clean exit, no output (all migrations applied)
- **Status:** PASS

#### TC-03 — Content model has new fields
- **Pre-condition:** Shell access
- **Steps:** Import Content model, print `_meta.get_fields()` names
- **Expected:** `preview_image_url` and `file` present in field list
- **Actual:** `['id', 'title', 'url', 'preview_image_url', 'content_type', 'description', 'status', 'file', 'user', 'category', 'created_at', 'updated_at', 'tags']`
- **Status:** PASS

#### TC-04 — LinkPreviewService returns empty dict gracefully on bad URL
- **Pre-condition:** `contents.services` importable
- **Steps:** Call `fetch_preview('')`, `fetch_preview('http://192.168.1.1/')`, `fetch_preview('http://127.0.0.1/secret')`
- **Expected:** All return `{'preview_image_url': None, 'og_title': None, 'og_description': None}`
- **Actual:** All three calls returned the expected safe empty dict. SSRF protection on empty string, private IP (192.168.x.x), and loopback (127.0.0.1) all working.
- **Status:** PASS

#### TC-05 — validate_file_extension rejects disallowed types
- **Pre-condition:** `contents.validators` importable
- **Steps:** Call `validate_file_extension` with a SimpleUploadedFile named `malware.exe`
- **Expected:** `ValidationError` raised
- **Actual:** `ValidationError: ['File type ".exe" is not allowed. Allowed formats: .doc, .docx, .gif, .jpeg, .jpg, .md, .mp3, .mp4, .pdf, .png, .txt, .webp']`
- **Status:** PASS

#### TC-06 — validate_file_extension allows valid types
- **Pre-condition:** `contents.validators` importable
- **Steps:** Call `validate_file_extension` with files named `file.pdf`, `file.jpg`, `file.png`, `file.mp3`, `file.docx`, `file.md`
- **Expected:** No exception raised for any extension
- **Actual:** All six extensions passed without exception
- **Status:** PASS

#### TC-07 — validate_file_size rejects files > 10MB
- **Pre-condition:** `contents.validators` importable
- **Steps:** Call `validate_file_size` with a 11MB SimpleUploadedFile
- **Expected:** `ValidationError` raised
- **Actual:** `ValidationError: ['File size must not exceed 10MB. Current size: 11.0 MB']`
- **Status:** PASS

#### TC-08 — get_card_image() returns placeholder path when no file/preview
- **Pre-condition:** Test user `qa7@test.com` created
- **Steps:** Create unsaved Content with `content_type='article'`, no file, no preview_image_url. Call `get_card_image()`.
- **Expected:** Return path contains `article.svg`
- **Actual:** `/static/images/placeholders/article.svg`
- **Status:** PASS

#### TC-09 — get_card_image() returns preview_image_url when set
- **Pre-condition:** Test user `qa7@test.com` exists
- **Steps:** Create unsaved Content with `preview_image_url='https://example.com/og.jpg'`. Call `get_card_image()`.
- **Expected:** Return `'https://example.com/og.jpg'`
- **Actual:** `'https://example.com/og.jpg'`
- **Status:** PASS

#### TC-10 — Signal registered (no error on import)
- **Pre-condition:** `contents.apps` importable
- **Steps:** Import `ContentsConfig`, print `ready` method
- **Expected:** Method reference printed without error
- **Actual:** `Signal app ready method: <function ContentsConfig.ready at 0x10b534c20>`
- **Status:** PASS

#### TC-11 — RefreshPreviewView rejects unauthenticated POST
- **Pre-condition:** No authenticated session
- **Steps:** POST to `/contents/1/refresh-preview/` without login
- **Expected:** HTTP 302 redirect to login page
- **Actual:** HTTP 302, Location: `/users/login/?next=/contents/1/refresh-preview/`
- **Status:** PASS

#### TC-12 — RefreshPreviewView rejects wrong user (user isolation)
- **Pre-condition:** Two users created; content owned by User A
- **Steps:** User B POSTs to User A's `/contents/{pk}/refresh-preview/`
- **Expected:** HTTP 404
- **Actual:** HTTP 404 (Not Found: `/contents/33/refresh-preview/`)
- **Status:** PASS

#### TC-13 — Content create form renders with file field (HTTP 200)
- **Pre-condition:** Authenticated as `qa7@test.com`
- **Steps:** GET `/contents/create/`
- **Expected:** HTTP 200, response body contains `id_file`
- **Actual:** HTTP 200, `id_file` present in response
- **Status:** PASS

#### TC-14 — Content form has enctype multipart
- **Pre-condition:** Authenticated as `qa7@test.com`
- **Steps:** GET `/contents/create/`, inspect response body
- **Expected:** `enctype` and `multipart/form-data` present in response
- **Actual:** Both strings present — form tag has `enctype='multipart/form-data'`
- **Status:** PASS

#### TC-15 — Content list renders with view toggle (HTTP 200)
- **Pre-condition:** Authenticated as `qa7@test.com`
- **Steps:** GET `/contents/`
- **Expected:** HTTP 200, `btn-view-cards` and `btn-view-list` present in body
- **Actual:** HTTP 200; both button IDs found in response body
- **Status:** PASS

#### TC-16 — Content card component exists and has correct structure
- **Pre-condition:** `templates/components/content_card.html` exists
- **Steps:** Static analysis of template file
- **Expected:** `get_card_image` called, `onerror` fallback present, `line-clamp-2` on title, type and status badge overlays present
- **Actual:** All five checks pass. `get_card_image` used correctly via `{{ content.get_card_image }}` (Django template callable resolution). `onerror="this.onerror=null; this.src=..."` fallback present. `line-clamp-2` on h3. Type badge at `absolute top-2 left-2`, status badge at `absolute top-2 right-2`.
- **Status:** PASS

#### TC-17 — Placeholder SVGs all exist
- **Pre-condition:** `static/images/placeholders/` directory exists
- **Steps:** Glob `static/images/placeholders/*.svg`
- **Expected:** All 7 files present: article.svg, video.svg, podcast.svg, course.svg, book.svg, tool.svg, other.svg
- **Actual:** All 7 files found: `/Users/mindera/github/studyhub/static/images/placeholders/article.svg`, video.svg, podcast.svg, course.svg, book.svg, tool.svg, other.svg
- **Status:** PASS

#### TC-18 — MEDIA_URL and MEDIA_ROOT in settings
- **Pre-condition:** Django settings importable
- **Steps:** Read `settings.MEDIA_URL` and `settings.MEDIA_ROOT`
- **Expected:** `MEDIA_URL == '/media/'`, `'media' in str(MEDIA_ROOT)`
- **Actual:** `MEDIA_URL: /media/`, `MEDIA_ROOT: /Users/mindera/github/studyhub/media`
- **Status:** PASS

#### TC-19 — File upload field in content form
- **Pre-condition:** `templates/contents/content_form.html` exists
- **Steps:** Static analysis of template
- **Expected:** `enctype='multipart/form-data'` on form tag, `{{ form.file }}` rendered, helper text about accepted formats, `id_file` change listener JS
- **Actual:** All four checks pass. Helper text: `"Accepted: PDF, JPG, PNG, GIF, WebP, MP3, MP4, DOC, DOCX, TXT, MD · Max: 10MB"`. JS `id_file` change listener with extension and size validation present.
- **Status:** PASS

#### TC-20 — Refresh preview button in edit form (static analysis)
- **Pre-condition:** `templates/contents/content_form.html` exists
- **Steps:** Static analysis of template
- **Expected:** `btn-refresh-preview` inside `{% if form.instance.pk and form.instance.url %}`, `data-url` with `contents:refresh_preview`, JS handler
- **Actual:** All four checks pass. Button is inside the correct conditional block. `data-url='{% url "contents:refresh_preview" form.instance.pk %}'`. JS `fetch` handler using POST with CSRF token present.
- **Status:** PASS

#### TC-21 — Download link on content detail (static analysis)
- **Pre-condition:** `templates/contents/content_detail.html` exists
- **Steps:** Static analysis of template
- **Expected:** `{% if content.file %}` block, download attribute, `content.file.url`
- **Actual:** All three checks pass. Block at line 83-96. `<a href='{{ content.file.url }}' download ...>Download File</a>`.
- **Status:** PASS

#### TC-22 — Content create with file upload (functional)
- **Pre-condition:** Test user `qa7@test.com` authenticated
- **Steps:** POST to `/contents/create/` with valid PDF SimpleUploadedFile, title `"My PDF"`, type `other`, status `new`
- **Expected:** HTTP 302 (successful form submission, redirect to detail page)
- **Actual:** HTTP 302
- **Status:** PASS

#### TC-23 — File extension rejection (server-side)
- **Pre-condition:** Test user `qa7@test.com` authenticated
- **Steps:** POST to `/contents/create/` with disallowed `.exe` file
- **Expected:** HTTP 200 (form re-rendered with validation error)
- **Actual:** HTTP 200; response body contains `not allowed` / `File type` error text confirming form validation error displayed
- **Status:** PASS

#### TC-24 — content_list.html view toggle localStorage JS
- **Pre-condition:** `templates/contents/content_list.html` exists
- **Steps:** Static analysis of JS block; compare `getElementById` call targets vs HTML `id` attributes
- **Expected:** `localStorage.getItem`/`setItem` present; default 'cards'; `view-cards-container` and `view-list-container` elements; JS getElementById targets match HTML ids
- **Actual:** localStorage calls present. Default is 'cards'. HTML container IDs are `view-cards-container` and `view-list-container`. **CRITICAL MISMATCH:** JS calls `getElementById('view-cards')` and `getElementById('view-list')` — these IDs do not exist. Both `cardView` and `listView` JS variables will be `null`. The `applyView()` function calls `.classList.toggle('hidden', ...)` on null objects, making all toggle logic inert. Both views will be simultaneously visible on every page load regardless of localStorage preference.
- **Status:** FAIL
- **See:** BUG-01

#### TC-25 — ALLOWED_UPLOAD_EXTENSIONS and MAX_UPLOAD_SIZE_MB in settings
- **Pre-condition:** Django settings importable
- **Steps:** Read `settings.ALLOWED_UPLOAD_EXTENSIONS` and `settings.MAX_UPLOAD_SIZE_MB`
- **Expected:** Extensions list present; `MAX_UPLOAD_SIZE_MB == 10`
- **Actual:** `['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp3', '.mp4', '.doc', '.docx', '.txt', '.md']`; `MAX_UPLOAD_SIZE_MB: 10`
- **Status:** PASS

---

### Design System Compliance Checks

#### DSC-01 — Video badge color: `red` vs `rose` (pre-existing bug tracking)
- **Components checked:** `content_detail.html` (line 40), `content_list.html` (line 154), `content_card.html` (line 18)
- **Finding:** `content_detail.html` and `content_list.html` (list view) use `bg-red-500/10 text-red-400` for the Video type badge. The design system spec at `docs/design-system.md` explicitly specifies `bg-rose-500/10 text-rose-400` for Video. `content_card.html` (card view overlay) correctly uses `bg-rose-500/80`.
- **Status:** WARN (pre-existing from Sprint 4/6, partially fixed in card component but not in detail/list views)
- **See:** BUG-02

---

### Bugs Found

#### BUG-01 — View toggle is non-functional: JS getElementById targets mismatched HTML element IDs
- **Severity:** High
- **Component:** `templates/contents/content_list.html`
- **Description:** The view toggle JavaScript block references `getElementById('view-cards')` and `getElementById('view-list')` to find the container divs. However, the actual HTML element IDs are `view-cards-container` and `view-list-container`. Since the JS variables `cardView` and `listView` resolve to `null`, the `applyView()` function silently fails on every call — no container is ever shown or hidden. The result is that both the card grid and the list view are simultaneously visible on every page load, and clicking the toggle buttons has no visual effect on the content area (only the button active-state styles change correctly, as those target `btn-view-cards` and `btn-view-list` which are correct).
- **Reproduction:**
  1. Log in as any user
  2. Navigate to `/contents/`
  3. Observe: both the card grid (`view-cards-container`) and the list view (`view-list-container`) are visible simultaneously
  4. Click the list toggle button — card grid does not hide
  5. Click the card toggle button — list view does not hide
  6. Refresh page — both views still visible (localStorage preference saved but ignored for DOM toggle)
- **Expected vs Actual:** Clicking the list toggle button should hide the card grid and show the list view, and vice versa. Actual: both views always rendered, toggle has no effect on container visibility.
- **Root cause:** In `content_list.html` script block, line 295: `var cardView = document.getElementById('view-cards')` should be `getElementById('view-cards-container')`. Line 296: `var listView = document.getElementById('view-list')` should be `getElementById('view-list-container')`.

#### BUG-02 — Video type badge uses `red` instead of `rose` in detail and list views (pre-existing)
- **Severity:** Medium
- **Component:** `templates/contents/content_detail.html` (line 40), `templates/contents/content_list.html` (line 154)
- **Description:** The Video content type badge uses `bg-red-500/10 text-red-400` in both the content detail page and the list view's list-mode badge column. The design system (`docs/design-system.md`) specifies `bg-rose-500/10 text-rose-400` for Video. This is a persisting regression first reported in Sprint 4. Note that `content_card.html` (the card grid overlay) was correctly updated to use `rose` in Sprint 7, creating an inconsistency between the three views.
- **Reproduction:**
  1. Log in and navigate to `/contents/`
  2. Switch to list view
  3. Observe a Video-type content item — badge reads `bg-red-500/10 text-red-400`
  4. Navigate to the detail page of any Video content
  5. Observe the Video type badge — `bg-red-500/10 text-red-400`
  6. Compare with card grid view which correctly shows `bg-rose-500/80`
- **Expected vs Actual:** All three views (card, list, detail) should render Video badge as `rose`. Actual: card view uses rose (correct), list and detail views use red (incorrect).
