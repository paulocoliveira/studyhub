---
name: Sprint 5 template structure
description: AI Insights panel, content form AI buttons, AJAX wiring, and dashboard Row 5 added in Sprint 5
type: project
---

Sprint 5 introduced AI features into the frontend via two template changes:

**templates/contents/content_form.html**
- Replaced the disabled AI placeholder section (dashed border card) with two live gradient buttons:
  - `#btn-suggest-category` — placed directly below the category select field, calls `insights:suggest_category` via POST
  - `#btn-generate-description` — placed directly below the description textarea, calls `insights:generate_description` via POST
- Both buttons carry `data-url` attributes set via `{% url %}` tags
- A `{% block scripts %}` block at the bottom of the template contains all AJAX logic (no external JS)
- `showAiError` appends a `.ai-error` `<p>` to `btn.parentElement` and auto-removes it after 5 seconds
- Category suggestion matches by case-insensitive text comparison against `<select>` options

**templates/insights/insights_panel.html**
- Standalone component (not extending base.html) — designed to be `{% include %}`'d
- Contains its own `<script>` block with an IIFE wrapping the generate-insights click handler
- Uses `simpleMarkdown()` helper to convert `**bold**`, `## headings`, `- bullets`, and newlines to HTML
- Three state elements: `#insights-result` (hidden by default), `#insights-placeholder` (visible by default), `#insights-error` (hidden by default)
- Button: `#btn-generate-insights` with `data-url='{% url "insights:generate_insights" %}'`

**templates/dashboard/dashboard.html**
- Row 4 `<section>` gained `class='mb-8'` for consistent spacing
- Row 5 added at the bottom: `{% include 'insights/insights_panel.html' %}` inside a `<section aria-label='AI Insights' class='mb-8'>`

**URL names used:**
- `insights:suggest_category` (POST)
- `insights:generate_description` (POST)
- `insights:generate_insights` (GET)

**Why:** Sprint 5 backend endpoints were being implemented in parallel; frontend wired to the agreed contract ({success, category/description/insights} or {success: false, error}).

**How to apply:** When extending AI features, reuse the `aiRequest` pattern from content_form.html or the IIFE fetch pattern from insights_panel.html. The panel is included-not-extended so it can be embedded anywhere without a full page context.
