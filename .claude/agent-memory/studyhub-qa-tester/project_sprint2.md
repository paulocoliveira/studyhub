---
name: Sprint 2 QA findings
description: Test results, bugs, and patterns discovered during Sprint 2 (Categories & Tags) QA
type: project
---

## Sprint 2 QA results (2026-03-25)

- 33 tests run: 31 PASS, 2 FAIL, 0 WARN
- All model-level tests (ORM, unique_together, __str__, cascade) passed
- All auth gate tests passed (unauthenticated redirects to login)
- All access-control isolation tests passed (user A cannot reach user B's objects)
- All template existence checks passed (6 templates confirmed present)
- CRUD flows for both categories and tags passed (create/edit/delete)

## BUG-01 — Critical: List views crash with HTTP 500 (Count('contents') annotation premature)

Both `CategoryListView` and `TagListView` call `.annotate(content_count=Count('contents'))`.
The 'contents' reverse FK relation on `Category` and `Tag` does not exist because `contents/models.py`
is empty in Sprint 2. Django raises `FieldError` at queryset build time → HTTP 500 on every
authenticated `/categories/` and `/tags/` page load.

**Status:** Open. Fix requires Sprint 3 to deliver `Content` model with `ForeignKey(Category)` and
`ManyToManyField(Tag)`, OR the annotation must be removed/guarded until then.

## Structural observations

- Tags have no edit/update view or URL (create + delete only). Categories have full CRUD.
  Confirm against PRD whether tag renaming is required.
- Admin registration for both models is correct and complete.
- `core/urls.py` correctly wires both apps with proper namespaces.

## Test script location

`/tmp/sprint2_tests.py` — run with `python manage.py shell < /tmp/sprint2_tests.py`
Uses `Client(raise_request_exception=False)` to catch 500 errors as response objects
rather than exceptions (critical for documenting server errors).
