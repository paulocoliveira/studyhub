---
name: Sprint 2 template structure
description: Template files, URL wiring, context variables, and conventions established in Sprint 2 (Categories & Tags)
type: project
---

Sprint 2 implements full CRUD templates for Categories and Tags.

**Why:** Sprint 1 had placeholder stub templates (`categories/list.html`, `tags/list.html`) using `TemplateView`. Sprint 2 replaces these with fully functional CBV-backed templates.

**How to apply:** Do not edit or reference the old `list.html` stubs — they remain as dead files from Sprint 1. The active templates are the Django CBV-named files below.

## Categories templates
- `templates/categories/category_list.html` — used by `CategoryListView` (template_name set explicitly)
- `templates/categories/category_form.html` — used by both `CategoryCreateView` and `CategoryUpdateView`
- `templates/categories/category_confirm_delete.html` — used by `CategoryDeleteView`

Context variables:
- `categories` — queryset annotated with `content_count` (from `Count('contents')`)
- `form` — `CategoryForm` (fields: name, description); widgets already have Tailwind classes set server-side
- `object` — Category instance on delete confirm and update views

## Tags templates
- `templates/tags/tag_list.html` — used by `TagListView`
- `templates/tags/tag_form.html` — used by `TagCreateView` (no update view for tags)
- `templates/tags/tag_confirm_delete.html` — used by `TagDeleteView`

Context variables:
- `tags` — queryset annotated with `content_count` (from `Count('contents')`)
- `form` — `TagForm` (field: name only); widget has Tailwind classes set server-side
- `object` — Tag instance on delete confirm

## URL names
- `categories:list`, `categories:create`, `categories:update pk`, `categories:delete pk`
- `tags:list`, `tags:create`, `tags:delete pk`
- All resolve correctly — verified with `reverse()` in Django shell

## Dead stub files (do not use)
- `templates/categories/list.html` — Sprint 1 stub, no longer referenced by any view
- `templates/tags/list.html` — Sprint 1 stub, no longer referenced by any view
