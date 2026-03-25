# Sprint 3 — Test Report
## StudyHub — Content Management

**Execution date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite · TailwindCSS CDN
**Method:** Django Test Client (automated script via `manage.py shell`) + static code analysis
**Executed by:** Claude Code (studyhub-qa-tester agent)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total tests | 34 |
| PASS | 34 |
| WARN | 0 |
| FAIL | 0 |
| Bugs found | 3 |
| Bugs fixed during sprint | 2 |
| Bugs pending (next sprint) | 1 |

**Overall result:** APPROVED — all tests pass after fixes. Full Content CRUD, filtering, search, sorting, status update, and pagination are functional with correct user-scoped data isolation.

---

## Test Scope

### Components tested

| Component | File | Status |
|-----------|------|--------|
| `Content` model + choices constants | `contents/models.py` | Tested |
| `ContentAdmin` | `contents/admin.py` | Tested |
| `ContentForm` | `contents/forms.py` | Tested |
| `ContentFilterForm` | `contents/forms.py` | Tested |
| `ContentListView` | `contents/views.py` | Tested |
| `ContentDetailView` | `contents/views.py` | Tested |
| `ContentCreateView` | `contents/views.py` | Tested |
| `ContentUpdateView` | `contents/views.py` | Tested |
| `ContentDeleteView` | `contents/views.py` | Tested |
| `ContentStatusUpdateView` | `contents/views.py` | Tested |
| URL routing | `contents/urls.py` | Tested |
| Template `content_list.html` | `templates/contents/content_list.html` | Tested |
| Template `content_detail.html` | `templates/contents/content_detail.html` | Tested |
| Template `content_form.html` | `templates/contents/content_form.html` | Tested |
| Template `content_confirm_delete.html` | `templates/contents/content_confirm_delete.html` | Tested |
| Template `components/pagination.html` | `templates/components/pagination.html` | Tested |
| Category `Count('contents')` re-enabled | `categories/views.py` | Tested |
| Tag `Count('contents')` re-enabled | `tags/views.py` | Tested |

### Out of scope (Sprint 4+)
- Dashboard content stats
- AI features (Sprint 5)

---

## Test Cases

### TC-01 — Django system check

| Field | Value |
|-------|-------|
| **ID** | TC-01 |
| **Expected** | 0 issues |
| **Actual** | 0 issues |
| **Status** | **PASS** |

---

### TC-02 — Migration applied

| Field | Value |
|-------|-------|
| **ID** | TC-02 |
| **Description** | `contents_content` table exists in DB |
| **Status** | **PASS** |

---

### TC-03 — Content __str__

| Field | Value |
|-------|-------|
| **ID** | TC-03 |
| **Description** | Create Content via ORM; `__str__` returns title |
| **Status** | **PASS** |

---

### TC-04 — Default status

| Field | Value |
|-------|-------|
| **ID** | TC-04 |
| **Description** | New Content has `status='new'` by default |
| **Status** | **PASS** |

---

### TC-05 — Ordering

| Field | Value |
|-------|-------|
| **ID** | TC-05 |
| **Description** | Content queryset is ordered by `-created_at` (newest first) |
| **Status** | **PASS** |

---

### TC-06 — SET_NULL on category delete

| Field | Value |
|-------|-------|
| **ID** | TC-06 |
| **Description** | Deleting a category sets `content.category = None`, content is NOT deleted |
| **Expected** | Content exists, `content.category is None` |
| **Actual** | Content exists, `content.category is None` |
| **Status** | **PASS** |

---

### TC-07 — Count annotation on Category

| Field | Value |
|-------|-------|
| **ID** | TC-07 |
| **Description** | `Category.objects.annotate(content_count=Count('contents'))` returns correct count |
| **Actual** | `content_count=3` for 3 contents linked to category |
| **Status** | **PASS** |

---

### TC-08 — Unauthenticated content list

| Field | Value |
|-------|-------|
| **ID** | TC-08 |
| **Expected** | HTTP 302 → `/users/login/?next=/contents/` |
| **Actual** | HTTP 302 |
| **Status** | **PASS** |

---

### TC-09 — Authenticated content list

| Field | Value |
|-------|-------|
| **ID** | TC-09 |
| **Expected** | HTTP 200 |
| **Actual** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-10 — Filter by status

| Field | Value |
|-------|-------|
| **ID** | TC-10 |
| **Input** | `GET /contents/?status=new` |
| **Expected** | HTTP 200, only `new` items in response |
| **Status** | **PASS** |

---

### TC-11 — Filter by search

| Field | Value |
|-------|-------|
| **ID** | TC-11 |
| **Input** | `GET /contents/?search=<title_fragment>` |
| **Expected** | HTTP 200, matching items only |
| **Initial result** | Broken — form sent `?search=` but view read `?q=` (BUG-01) |
| **After fix** | HTTP 200, matching items returned |
| **Bug associated** | B-01 (fixed) |
| **Status** | **PASS** |

---

### TC-12 — Filter by content_type

| Field | Value |
|-------|-------|
| **ID** | TC-12 |
| **Input** | `GET /contents/?content_type=article` |
| **Status** | **PASS** |

---

### TC-13 — Filter by category

| Field | Value |
|-------|-------|
| **ID** | TC-13 |
| **Input** | `GET /contents/?category=<id>` |
| **Status** | **PASS** |

---

### TC-14 — Pagination

| Field | Value |
|-------|-------|
| **ID** | TC-14 |
| **Description** | 13 items created; list shows 12 + next page link present |
| **Status** | **PASS** |

---

### TC-15 — Create page

| Field | Value |
|-------|-------|
| **ID** | TC-15 |
| **Input** | `GET /contents/create/` |
| **Expected** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-16 — Create content

| Field | Value |
|-------|-------|
| **ID** | TC-16 |
| **Input** | `POST /contents/create/` with `title`, `content_type`, `status` |
| **Expected** | HTTP 302 → `/contents/` |
| **Status** | **PASS** |

---

### TC-17 — Content persisted

| Field | Value |
|-------|-------|
| **ID** | TC-17 |
| **Description** | Content exists in DB after TC-16 |
| **Status** | **PASS** |

---

### TC-18 — Detail page

| Field | Value |
|-------|-------|
| **ID** | TC-18 |
| **Input** | `GET /contents/<pk>/` |
| **Expected** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-19 — Edit page

| Field | Value |
|-------|-------|
| **ID** | TC-19 |
| **Input** | `GET /contents/<pk>/edit/` |
| **Expected** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-20 — Update content

| Field | Value |
|-------|-------|
| **ID** | TC-20 |
| **Input** | `POST /contents/<pk>/edit/` with updated title |
| **Expected** | HTTP 302 → detail, title changed in DB |
| **Status** | **PASS** |

---

### TC-21 — Delete confirmation page

| Field | Value |
|-------|-------|
| **ID** | TC-21 |
| **Input** | `GET /contents/<pk>/delete/` |
| **Expected** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-22 — Delete content

| Field | Value |
|-------|-------|
| **ID** | TC-22 |
| **Input** | `POST /contents/<pk>/delete/` |
| **Expected** | HTTP 302 → list, content removed from DB |
| **Status** | **PASS** |

---

### TC-23 — Cross-user isolation

| Field | Value |
|-------|-------|
| **ID** | TC-23 |
| **Description** | User B accessing User A's content detail/edit/delete → HTTP 404 |
| **Status** | **PASS** |

---

### TC-24 — Status update (valid)

| Field | Value |
|-------|-------|
| **ID** | TC-24 |
| **Input** | `POST /contents/<pk>/status/` with `status=completed` |
| **Expected** | HTTP 302, `content.status == 'completed'` in DB |
| **Status** | **PASS** |

---

### TC-25 — Status update (invalid value)

| Field | Value |
|-------|-------|
| **ID** | TC-25 |
| **Input** | `POST /contents/<pk>/status/` with `status=invalid_value` |
| **Expected** | HTTP 302, status unchanged |
| **Status** | **PASS** |

---

### TC-26 — Unauthenticated status update

| Field | Value |
|-------|-------|
| **ID** | TC-26 |
| **Input** | `POST /contents/<pk>/status/` without session |
| **Expected** | HTTP 302 → login |
| **Status** | **PASS** |

---

### TC-27 to TC-31 — Template files exist

| TC | Template | Status |
|----|----------|--------|
| TC-27 | `templates/contents/content_list.html` | **PASS** |
| TC-28 | `templates/contents/content_detail.html` | **PASS** |
| TC-29 | `templates/contents/content_form.html` | **PASS** |
| TC-30 | `templates/contents/content_confirm_delete.html` | **PASS** |
| TC-31 | `templates/components/pagination.html` | **PASS** |

---

### TC-32 — Categories list (Count re-enabled)

| Field | Value |
|-------|-------|
| **ID** | TC-32 |
| **Description** | `GET /categories/` → HTTP 200 with correct content_count |
| **Status** | **PASS** |

---

### TC-33 — Tags list (Count re-enabled)

| Field | Value |
|-------|-------|
| **ID** | TC-33 |
| **Description** | `GET /tags/` → HTTP 200 with correct content_count |
| **Status** | **PASS** |

---

## Bugs Found During Testing

| ID | Priority | Status | Description |
|----|----------|--------|-------------|
| B-01 | High | Fixed | Search field name mismatch: form submitted `?search=` but view read `?q=` |
| B-02 | Low | Fixed | Delete button used `bg-red-600` instead of `bg-rose-600` design system color |
| B-03 | Low | Deferred | Status badge color naming (blue/yellow/green vs sky/amber/emerald) — design system allows both, no functional impact |

> Full details in `SPRINT3_BUG_REPORT.md`

---

## Task Coverage

| Task | Description | Tested | Result |
|------|-------------|--------|--------|
| 3.1 | Create Contents App (model, admin, migrations) | Yes | PASS |
| 3.2 | Content Forms | Yes | PASS |
| 3.3 | Content Views + URLs | Yes | PASS |
| 3.4 | Content Templates + Pagination component | Yes | PASS |

---

## Test Environment

```
Operating system    : macOS Darwin 25.3.0
Python              : 3.13
Django              : 6.0.3
Database            : SQLite (db.sqlite3)
AUTH_USER_MODEL     : users.CustomUser
```
