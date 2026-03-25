---
name: Sprint 1 template structure
description: Template files, URL wiring, and stub views established in Sprint 1
type: project
---

Sprint 1 established the full template skeleton for StudyHub.

**Why:** Sprint 1 task list required base templates, auth templates, landing page, and a placeholder dashboard to make the login-redirect flow functional end-to-end.

**How to apply:** When working on later sprints, these templates already exist and should be extended/refined rather than recreated. The placeholder templates (contents/list, categories/list, tags/list, insights/index) are intentional stubs to be filled in later sprints.

## Template locations
- `templates/base.html` — authenticated layout (sidebar + topbar + flash messages)
- `templates/base_public.html` — public layout (no sidebar)
- `templates/components/sidebar.html` — sidebar nav with active-state detection via `request.path|slice`
- `templates/components/topbar.html` — top bar with page_title block, user email, logout form
- `templates/components/messages.html` — dismissible flash messages (success/error/warning/info)
- `templates/landing.html` — public landing page (hero, features, CTA banner, footer)
- `templates/users/register.html` — registration form
- `templates/users/login.html` — login form
- `templates/users/password_change.html` — password change form
- `templates/dashboard/dashboard.html` — placeholder dashboard (Sprint 4 placeholder)
- `templates/contents/list.html` — placeholder (Sprint 2)
- `templates/categories/list.html` — placeholder (Sprint 3)
- `templates/tags/list.html` — placeholder (Sprint 3)
- `templates/insights/index.html` — placeholder (Sprint 5)

## Active state detection in sidebar
Uses `request.path|slice` comparison rather than `{% url %}` equality because Django's `{% url %}` tag returns the path without a way to compare directly in DTL conditionals with prefix matching. Pattern: `{% if request.path|slice:":9" == "/contents" %}`.

## URL namespace note
All app URL configs define `app_name` directly in `urls.py`. `core/urls.py` uses `include('app.urls', namespace='app')` which overrides. Both are set consistently — no double-namespace issue.

## Stub views added for sidebar URL resolution
These apps had empty `urlpatterns = []` and needed at least one named URL for the sidebar to render without `NoReverseMatch`:
- `contents`: `ContentListView` at `contents:list`
- `categories`: `CategoryListView` at `categories:list`
- `tags`: `TagListView` at `tags:list`
- `insights`: `InsightsIndexView` at `insights:index`
