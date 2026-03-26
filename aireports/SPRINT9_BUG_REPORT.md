# Sprint 9 — Bug Report
## StudyHub — Automated Testing Pass

**Date:** 2026-03-26
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis during Sprint 9 test implementation
**Total bugs:** 2
**Fixed:** 2 (during Sprint 9)

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | High | `categories/forms.py`, `categories/views.py` | Fixed |
| [B-02](#b-02) | High | `tags/forms.py`, `tags/views.py` | Fixed |

---

## B-01

**Title:** Duplicate category name for same user raises unhandled `IntegrityError` (HTTP 500) instead of form validation error

**Severity:** High
**Component:** `categories/forms.py`, `categories/views.py`
**Status:** Fixed
**Discovered in:** Sprint 9 automated test — `test_duplicate_category_name_fails`
**Fix date:** 2026-03-26

### Description

When an authenticated user attempts to create a second category with a name identical to one they already have, the application responds with an unhandled `IntegrityError` (HTTP 500) instead of returning the form with a validation error. The `unique_together = ['name', 'user']` constraint exists at the database level, but was never enforced at the Django form level.

### Steps to reproduce

1. Log in as any user
2. Create a category named "Python"
3. Navigate to `/categories/create/`
4. Submit the form again with the name "Python"
5. Observe HTTP 500 — `UNIQUE constraint failed: categories_category.name, categories_category.user_id`

### Expected behavior

The form re-renders with a validation error: `"A category with this name already exists."` — HTTP 200 with an inline error message.

### Actual behavior

```
django.db.utils.IntegrityError: UNIQUE constraint failed:
    categories_category.name, categories_category.user_id
```
Django raises an unhandled exception. The error page is shown (or a 500 in production).

### Root cause

`CategoryForm` is a `ModelForm` with `fields = ['name', 'description']`. The `user` field is intentionally excluded because it is set programmatically in `CategoryCreateView.form_valid()`. However, Django's `ModelForm.validate_unique()` calls `instance.validate_unique()` internally to check `unique_together` constraints. At the time `is_valid()` runs, `instance.user` is still `None` (it has not been assigned yet), so Django silently skips the `unique_together` check (the constraint cannot be evaluated without both fields). The form passes validation, `super().form_valid()` calls `save()`, and the database raises the integrity error.

### Fix applied

**Files:** `categories/forms.py`, `categories/views.py`

`CategoryForm` now accepts a `user` keyword argument in `__init__` and overrides `validate_unique()` to temporarily set `self.instance.user` before calling the parent method, so Django can evaluate the full `['name', 'user']` constraint at form validation time.

```python
# categories/forms.py — before
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        ...

# categories/forms.py — after
class CategoryForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def validate_unique(self):
        if self._user is not None:
            self.instance.user = self._user
        super().validate_unique()

    class Meta:
        model = Category
        fields = ['name', 'description']
        ...
```

`CategoryCreateView` and `CategoryUpdateView` now override `get_form_kwargs()` to pass `user=self.request.user` to the form constructor.

```python
# categories/views.py — added to both CreateView and UpdateView
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
```

### Impact

Any user who attempts to create a duplicate category name is shown an HTTP 500 error. This is a poor user experience and, in a production environment with `DEBUG=False`, would expose a generic server error page with no actionable feedback. The constraint is also invisible in the UI, making the system appear broken rather than correctly validating input.

---

## B-02

**Title:** Duplicate tag name for same user raises unhandled `IntegrityError` (HTTP 500) instead of form validation error

**Severity:** High
**Component:** `tags/forms.py`, `tags/views.py`
**Status:** Fixed
**Discovered in:** Sprint 9 automated test — `test_duplicate_tag_name_fails`
**Fix date:** 2026-03-26

### Description

Identical root cause to B-01, but affecting the `Tag` model. The `unique_together = ['name', 'user']` constraint on `Tag` is enforced at the database level but bypassed at form validation time, causing an unhandled `IntegrityError` (HTTP 500) when a user attempts to create a tag with a name they already use.

### Steps to reproduce

1. Log in as any user
2. Create a tag named "django"
3. Navigate to `/tags/create/`
4. Submit the form again with the name "django"
5. Observe HTTP 500 — `UNIQUE constraint failed: tags_tag.name, tags_tag.user_id`

### Expected behavior

The form re-renders with a validation error: `"A tag with this name already exists."` — HTTP 200 with inline error.

### Actual behavior

```
django.db.utils.IntegrityError: UNIQUE constraint failed:
    tags_tag.name, tags_tag.user_id
```

### Root cause

Same as B-01: `TagForm` excludes `user` from its fields. When `is_valid()` runs, `instance.user` is `None`, so `validate_unique()` cannot check the `unique_together` constraint and silently skips it. The form passes, `save()` runs, and the database rejects the insert.

### Fix applied

**Files:** `tags/forms.py`, `tags/views.py`

Same fix pattern as B-01:

```python
# tags/forms.py — after
class TagForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def validate_unique(self):
        if self._user is not None:
            self.instance.user = self._user
        super().validate_unique()

    class Meta:
        model = Tag
        fields = ['name']
        ...
```

```python
# tags/views.py — added to TagCreateView
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
```

### Impact

Same as B-01. Any user attempting to create a duplicate tag receives an HTTP 500 instead of a friendly validation error. This undermines trust in the application and would be a visible failure in a production environment.

---

## Fix Summary

| ID | Modified files | Change | Migration needed |
|----|---------------|--------|-----------------|
| B-01 | `categories/forms.py`, `categories/views.py` | Added `user` injection in form `__init__` + `validate_unique` override; `get_form_kwargs` in both Create and Update views | No |
| B-02 | `tags/forms.py`, `tags/views.py` | Same fix pattern as B-01 | No |
