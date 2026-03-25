# Sprint 6 — Bug Report
## StudyHub — Polish & Refinements

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 2
**Fixed:** 2 (during QA)
**Pending:** 0

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Medium | `templates/contents/content_form.html` | Fixed |
| [B-02](#b-02) | Medium | `templates/contents/content_list.html` · `templates/contents/content_detail.html` | Fixed |

---

## B-01

**Title:** Client-side form validation missing — `novalidate` set but no JS submit handler

**Severity:** Medium
**Component:** `templates/contents/content_form.html`
**Status:** Fixed
**Discovered in:** TC-17 (client-side validation in content form)
**Fix date:** 2026-03-25

### Description

Sprint 6.5.2 required client-side validation to replace browser-native validation (`novalidate` attribute added to `<form>`). The `novalidate` attribute was correctly placed, disabling the browser's built-in required-field enforcement. However, no JavaScript submit handler was added to replace it. As a result, submitting a blank title field caused a silent POST to the server with no client-side feedback — the user only saw a server-side validation error after a full page reload.

### Steps to reproduce

1. Log in and go to `/contents/create/`
2. Leave the Title field blank
3. Click the Save button
4. Observe: form is submitted to the server with no client-side error message shown

### Expected behavior

A red error message "Title is required." appears below the Title input immediately (before any POST is sent), the input gets a `border-red-500` highlight, and the page scrolls to the error. Same for the Content Type field if left empty.

### Actual behavior

Form posts to the server silently. Server-side validation returns the error, but the UX round-trip is slow and the error appears only after a full page reload.

### Root cause

`novalidate` was added to the form by the sprint implementation to disable browser validation, but the JavaScript replacement (submit event listener) was not added to the `{% block scripts %}` block. The AI generate / URL-detect JS was present, but the validation handler was absent.

### Fix applied

**File:** `templates/contents/content_form.html`

Added a submit event listener inside `{% block scripts %}` that:
- Clears previous `.field-error` elements and `border-red-500` states
- Validates `id_title` (must not be blank) and `id_content_type` (must be non-empty)
- On failure: injects `.field-error` paragraphs below invalid inputs, adds `border-red-500`, calls `e.preventDefault()`, and smooth-scrolls to the first error
- Attaches `input` event listeners on both required fields to clear their error state as the user starts typing

### Impact

Without the fix, `novalidate` actively made UX worse: it removed browser validation without providing a JS replacement, so users got less feedback than before. Any user submitting an empty title experienced a server round-trip with no immediate feedback.

---

## B-02

**Title:** Status badge colors use wrong Tailwind palette in content list and detail pages

**Severity:** Medium
**Component:** `templates/contents/content_list.html` · `templates/contents/content_detail.html`
**Status:** Fixed
**Discovered in:** TC — Design consistency audit (Sprint 6.6.1)
**Fix date:** 2026-03-25

### Description

The design system defines specific Tailwind palette tokens for status badges:
- `new` → `sky` (`bg-sky-500/10 text-sky-400`)
- `in_progress` → `amber` (`bg-amber-500/10 text-amber-400`)
- `completed` → `emerald` (`bg-emerald-500/10 text-emerald-400`)

`content_list.html` and `content_detail.html` used `blue`, `yellow`, and `green` respectively — visually similar but incorrect palette tokens. The dashboard template (`dashboard.html`) had already been corrected in Sprint 4, creating an inconsistency where the same status rendered with different colors depending on which page the user was on.

### Steps to reproduce

1. Create content items with statuses `new`, `in_progress`, and `completed`
2. Compare the status badge colors on:
   - `/dashboard/` — correct (sky/amber/emerald)
   - `/contents/` — incorrect (blue/yellow/green)
   - `/contents/{pk}/` — incorrect (blue/yellow/green)

### Expected behavior

Status badges use identical colors on every page: sky for new, amber for in_progress, emerald for completed.

### Actual behavior

```
dashboard:     bg-sky-500/10 text-sky-400       ✓
content_list:  bg-blue-500/10 text-blue-400     ✗
content_detail: bg-blue-500/10 text-blue-400    ✗
```

### Root cause

The badge colors were originally authored with `blue`/`yellow`/`green` in the content list and detail templates (Sprint 3). The Sprint 4 fix corrected the dashboard template only. The Sprint 6 design consistency audit (`6.6.1`) did not catch these regressions because the agent confirmed the audit complete without identifying the residual violations.

### Fix applied

**Files:** `templates/contents/content_list.html`, `templates/contents/content_detail.html`

Replaced all status badge color tokens throughout both templates (card grid view, list view, quick-status-update buttons, header badge, action buttons):

```
# Before → After
bg-blue-500/10 text-blue-400 border-blue-500/20   →   bg-sky-500/10 text-sky-400 border-sky-500/20
bg-yellow-500/10 text-yellow-400 border-yellow-500/20   →   bg-amber-500/10 text-amber-400 border-amber-500/20
bg-green-500/10 text-green-400 border-green-500/20   →   bg-emerald-500/10 text-emerald-400 border-emerald-500/20
```

No non-status-badge colors (category badges, content type badges, delete/error UI) were modified.

### Impact

Visual inconsistency: the same "New" status appeared sky-blue on the dashboard and darker blue on the content list. Users who learned the color coding from the dashboard would see unexpected colors elsewhere. Medium impact: no functional breakage, but undermines the design system's visual language.

---

## Fix Summary

| ID | Modified file | Change | Migration needed |
|----|--------------|--------|-----------------|
| B-01 | `templates/contents/content_form.html` | Added JS submit validation handler with required-field checks, error state injection, and input-listener cleanup | No |
| B-02 | `templates/contents/content_list.html` | `blue`/`yellow`/`green` → `sky`/`amber`/`emerald` on all status badge occurrences | No |
| B-02 | `templates/contents/content_detail.html` | Same color token replacements for status badges | No |
