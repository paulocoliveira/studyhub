---
name: Sprint 3 — Content model and CRUD
description: What was built in Sprint 3: Content model, forms, views, URLs, and count annotation re-enablement
type: project
---

Sprint 3 implemented the full Content CRUD backend.

Key decisions made:
- `CONTENT_TYPE_CHOICES` in the task spec differ slightly from `docs/data-schema.md` (spec omits social_media_post/social_media_profile/pdf and adds book/tool). The task spec choices were used as the authoritative source for Sprint 3.
- `ContentFilterForm` uses GET param `q` for search (not `search`) — the `get_queryset` in `ContentListView` reads `request.GET.get('q')`.
- `ContentStatusUpdateView` uses `content.save(update_fields=['status', 'updated_at'])` for efficient partial saves.
- `Count('contents')` annotation was re-added to `CategoryListView` and `TagListView` after the Content model was created with `related_name='contents'` on both FK and M2M fields.
- Templates use `{{ category.content_count }}` and `{{ tag.content_count }}` with the `pluralize` filter.

**Why:** Content is the core model — categories, tags, and dashboard all depend on it.
**How to apply:** When building dashboard stats or insights features, Content is queryable via `Content.objects.filter(user=...)` with full filter/sort support already built into `ContentListView.get_queryset`.
