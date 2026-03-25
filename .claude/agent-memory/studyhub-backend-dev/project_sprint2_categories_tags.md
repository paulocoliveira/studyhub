---
name: Sprint 2 — Categories and Tags backend
description: Models, views, forms, admin, and URLs for categories and tags apps implemented in Sprint 2
type: project
---

Sprint 2 implemented full CRUD backends for the `categories` and `tags` apps.

**Category model** — `categories/models.py`: CharField name (max 100), TextField description (blank), FK to AUTH_USER_MODEL with related_name='categories', unique_together=['name','user'], ordering=['name'].

**Tag model** — `tags/models.py`: CharField name (max 50), FK to AUTH_USER_MODEL with related_name='tags', unique_together=['name','user'], ordering=['name'].

Both models have `created_at` / `updated_at`.

**Note:** The `related_name='contents'` on the Category→Content FK and Tag→Content M2M is set on the *Content* model side (Sprint 3). The Count('contents') annotation in CategoryListView and TagListView relies on that related_name being set when the Content model is created.

**Views pattern:** All CBVs with LoginRequiredMixin. `get_queryset()` always filters by `request.user`. `form_valid()` sets `form.instance.user = request.user` on Create views. Success messages via `django.contrib.messages`.

**DeleteView pattern:** `form_valid()` is the correct override (not `delete()`) for adding a success message before redirect in Django's `DeleteView`.

**Why:** Data isolation — users must never see each other's categories or tags.

**How to apply:** Follow same pattern for any future user-scoped CRUD app.
