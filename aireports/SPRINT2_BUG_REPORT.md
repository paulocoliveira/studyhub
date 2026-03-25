# Sprint 2 — Bug Report
## StudyHub — Categories & Tags

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 1
**Fixed:** 1 (during QA)
**Pending:** 0

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Critical | `categories/views.py`, `tags/views.py` | Fixed |

---

## B-01

**Title:** `Count('contents')` annotation crashes list views with `FieldError` — Content model not yet implemented

**Severity:** Critical
**Components:** `categories/views.py` (CategoryListView), `tags/views.py` (TagListView)
**Status:** Fixed
**Discovered in:** TC-08, TC-21
**Fix date:** 2026-03-25

### Description

Both `CategoryListView.get_queryset()` and `TagListView.get_queryset()` applied a `.annotate(content_count=Count('contents'))` to count related content items. However, the `Content` model is not implemented until Sprint 3 — meaning no FK from `Content` to `Category` and no M2M from `Content` to `Tag` exists yet. Django raised an unhandled `FieldError: Cannot resolve keyword 'contents' into field` at queryset build time, returning HTTP 500 on every authenticated request to the category and tag list pages.

### Steps to reproduce

```bash
source .venv/bin/activate && python manage.py runserver
# Log in, navigate to http://127.0.0.1:8000/categories/
# HTTP 500 — FieldError in server log
```

```python
# From Django shell:
from django.test import Client
from users.models import CustomUser
u = CustomUser.objects.create_user(email='test@x.com', password='Test1234!')
c = Client()
c.login(username='test@x.com', password='Test1234!')
print(c.get('/categories/').status_code)  # 500
```

### Expected behavior

HTTP 200 with an empty list (no categories yet).

### Actual behavior

```
HTTP 500 Internal Server Error
django.core.exceptions.FieldError: Cannot resolve keyword 'contents' into field.
Choices are: created_at, description, id, name, updated_at, user, user_id
```

### Root cause

`categories/views.py` and `tags/views.py` included a premature annotation:

```python
# categories/views.py — BEFORE fix
def get_queryset(self):
    return (
        Category.objects.filter(user=self.request.user)
        .annotate(content_count=Count('contents'))  # 'contents' reverse FK doesn't exist yet
    )
```

The `Count('contents')` traverses the reverse FK relation named `contents` which is expected to be set as `related_name='contents'` on `Content.category` (ForeignKey) — but that model is Sprint 3 work.

### Fix applied

**Files:** `categories/views.py`, `tags/views.py`

Removed the premature annotation. Content counts will be re-added in Sprint 3 once the `Content` model defines `category = ForeignKey(Category, related_name='contents', ...)` and `tags = ManyToManyField(Tag, related_name='contents', ...)`.

```python
# categories/views.py — AFTER fix
def get_queryset(self):
    return Category.objects.filter(user=self.request.user)

# tags/views.py — AFTER fix
def get_queryset(self):
    return Tag.objects.filter(user=self.request.user)
```

Also removed the now-unused `from django.db.models import Count` import from both files.

Also updated both list templates to show `0 contents` as a static placeholder badge instead of `{{ category.content_count }}` / `{{ tag.content_count }}`, which would silently render empty without the annotation. The badge will be made dynamic in Sprint 3.

### Impact

Critical: both main list pages (`/categories/` and `/tags/`) returned HTTP 500 for all authenticated users, making the entire sprint's UI inaccessible before the fix.

---

## Fix Summary

| ID | Files modified | Change | Migration needed |
|----|---------------|--------|-----------------|
| B-01 | `categories/views.py`, `tags/views.py`, `templates/categories/category_list.html`, `templates/tags/tag_list.html` | Removed premature `Count('contents')` annotation and static placeholder in templates | No |
