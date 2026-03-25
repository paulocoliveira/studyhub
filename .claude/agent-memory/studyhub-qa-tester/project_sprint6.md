---
name: Sprint 6 QA findings
description: Sprint 6 (Polish & Refinements) QA results — 21 pass, 2 fail, 2 warn; client-side validation absent; status badge regression persists
type: project
---

## Sprint 6 QA — 2026-03-25

**Result:** 21 PASS / 2 FAIL / 2 WARN out of 25 TCs.

### BUG-01 (Medium) — Client-side validation missing
`content_form.html` has `novalidate` on the form but no submit event listener to replace browser validation. Title field submits blank with no client-side error. JS block only contains AI button handlers and URL auto-detect. Sprint 6.5 spec required a submit listener + error CSS class injection.

### BUG-02 (Medium) — Status badge color regression (persists from Sprint 4)
`content_list.html` and `content_detail.html` both use `blue/yellow/green` for New/In Progress/Completed status badges. Design system requires `sky/amber/emerald`. Dashboard correctly uses `sky/amber/emerald`. This was filed in Sprint 4 and remains unresolved.
- Affected lines: `content_list.html` 176-188, 277-316, 349-355; `content_detail.html` 55-59, 163-196.

### WARN-01 — Breadcrumbs component unused
`templates/components/breadcrumbs.html` was created correctly but all page templates implement breadcrumbs inline. The component is dead code.

### WARN-02 — Tag picker is CSS-driven checkboxes, not JS pill picker
Sprint spec said hidden select + JS. Actual implementation uses Django's CheckboxSelectMultiple with `group-has-[:checked]` Tailwind CSS. Functionally correct.

### What passed cleanly
- All 7 main pages return 200 with no TemplateSyntaxErrors
- Empty states: dashboard (Welcome to StudyHub!), contents list, categories list, tags list — all correct
- Flash messages: `data-message` attr + 5000ms setTimeout fade present
- Mobile sidebar: hamburger with md:hidden, overlay/backdrop, openMobileSidebar/closeMobileSidebar JS, DOMContentLoaded auto-close on nav link click
- URL auto-detect: blur event on #id_url, YouTube+other regexes, guards against overwriting user selection
- Breadcrumbs: all four pages (content form/detail, category form, tag form) have working inline breadcrumbs with correct hierarchy
- Back links: all four pages have back link with left-arrow chevron
- Sidebar active state: uses `dashboard:home`, correct slice lengths for all sections
- Dashboard onboarding: `{% if stats.total_contents == 0 %}` with 3 quick-start cards
- CRUD messages: messages.success in all form_valid/delete_view for all three apps
- All CRUD 302 redirects functional
- Auth gates redirect unauthenticated users (302) for all protected routes
