---
name: Sprint 4 template structure
description: Dashboard template implemented in Sprint 4 — context vars, by_type dict quirk, and content-type badge mapping
type: project
---

Sprint 4 implements the full dashboard at `templates/dashboard/dashboard.html`, replacing the Sprint 1–3 placeholder.

**Why:** The placeholder told users to wait for Sprint 4. Sprint 4 wires up `DashboardService` and renders real stats.

**How to apply:** When editing the dashboard template or the service, be aware of the by_type quirk below.

## Dashboard template
- `templates/dashboard/dashboard.html` — used by `DashboardView` (template_name)

Context variables from `DashboardView.get_context_data`:
- `stats` — dict with keys:
  - `total_contents` — int
  - `by_status` — dict keyed by status value string ('new', 'in_progress', 'completed')
  - `by_type` — **list of plain dicts** `[{'content_type': str, 'count': int}]` — NOT model instances. Cannot call `.get_content_type_display()`. Must use `{% if item.content_type == 'article' %}` branches.
- `recent_added` — QuerySet of up to 5 Content objects ordered by `-created_at`
- `recent_completed` — QuerySet of up to 5 Content objects (status='completed') ordered by `-updated_at`
- `top_categories` — QuerySet of Category objects annotated with `content_count`, ordered by `-content_count`
- `top_tags` — QuerySet of Tag objects annotated with `content_count`, ordered by `-content_count`

## Content-type badge color mapping (matches content_list.html exactly)
- article → `bg-violet-500/10 text-violet-400`
- video → `bg-red-500/10 text-red-400`
- podcast → `bg-orange-500/10 text-orange-400`
- course → `bg-cyan-500/10 text-cyan-400`
- book → `bg-emerald-500/10 text-emerald-400`
- tool → `bg-pink-500/10 text-pink-400`
- other/fallback → `bg-gray-500/10 text-gray-400`

## Status badge color mapping
- new → `bg-blue-500/10 text-blue-400 border border-blue-500/20`
- in_progress → `bg-yellow-500/10 text-yellow-400 border border-yellow-500/20`
- completed → `bg-green-500/10 text-green-400 border border-green-500/20`

## URL names used in dashboard
- `contents:list`, `contents:create`, `contents:detail pk`
- `categories:list`, `categories:create`
- `tags:list`, `tags:create`
