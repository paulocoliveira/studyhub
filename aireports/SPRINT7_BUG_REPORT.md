# Sprint 7 — Bug Report
## StudyHub — Content Cards, Link Previews & File Upload

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
| [B-01](#b-01) | High | `templates/contents/content_list.html` | Fixed |
| [B-02](#b-02) | Medium | `templates/contents/content_detail.html` · `templates/contents/content_list.html` | Fixed |

---

## B-01

**Title:** View toggle non-functional — JS targets wrong element IDs for container divs

**Severity:** High
**Component:** `templates/contents/content_list.html` — view toggle JavaScript block
**Status:** Fixed
**Discovered in:** TC-24 (view toggle localStorage JS)
**Fix date:** 2026-03-25

### Description

The view toggle feature (cards / list) was completely non-functional. Both content views (card grid and list) were rendered simultaneously on every page load, and clicking the toggle buttons had no effect on container visibility. The localStorage preference was correctly saved and read, but the `applyView()` function that was supposed to show/hide the containers was a no-op because both DOM lookups resolved to `null`.

### Steps to reproduce

1. Log in and navigate to `/contents/`
2. Observe both the card grid and the list items visible at the same time
3. Click the list-view toggle button — card grid remains visible
4. Click the card-view toggle button — list view remains visible
5. Inspect the page source: confirm containers have IDs `view-cards-container` and `view-list-container`

### Expected behavior

Clicking the card toggle hides the list container and shows the card grid. Clicking the list toggle does the reverse. The chosen preference persists across page reloads via `localStorage`.

### Actual behavior

Both containers rendered simultaneously. Toggle buttons update their own active styling correctly but the content containers are never shown or hidden.

### Root cause

The JavaScript block used `getElementById('view-cards')` and `getElementById('view-list')` to locate the container divs, but the actual HTML element IDs are `view-cards-container` and `view-list-container`. Both lookups returned `null`, making every `classList.toggle()` call silently fail.

```javascript
// Before (broken)
var cardView = document.getElementById('view-cards');
var listView = document.getElementById('view-list');

// After (fixed)
var cardView = document.getElementById('view-cards-container');
var listView = document.getElementById('view-list-container');
```

### Fix applied

**File:** `templates/contents/content_list.html`

Updated the two `getElementById` calls in the view toggle IIFE to use the correct IDs (`view-cards-container` and `view-list-container`).

### Impact

Critical UX regression: the view toggle was the primary Sprint 7 feature visible to users. Both views displayed simultaneously created a broken, duplicate-content layout. The fix is two-character changes but the symptom was total feature failure.

---

## B-02

**Title:** Video content type badge uses `red` instead of `rose` in detail and list views

**Severity:** Medium
**Component:** `templates/contents/content_detail.html` · `templates/contents/content_list.html`
**Status:** Fixed
**Discovered in:** Design system compliance check (Sprint 7 QA)
**Fix date:** 2026-03-25

### Description

The Video content type badge used `bg-red-500/10 text-red-400` in the content detail page and content list (list mode). The design system specifies `bg-rose-500/10 text-rose-400` for the Video type. Sprint 7 correctly implemented `rose` in the new `content_card.html` component, but this created a three-way inconsistency:
- Card overlay badge: `rose` ✓
- List-mode badge: `red` ✗
- Detail page badge: `red` ✗

This bug has been present since Sprint 3 and flagged in Sprint 4, Sprint 6, and now Sprint 7 without full resolution.

### Steps to reproduce

1. Create a content item with type "Video"
2. Navigate to `/contents/` in card view — badge shows rose (correct)
3. Switch to list view — badge shows red (incorrect)
4. Click into the detail page — Video type badge shows red (incorrect)

### Expected behavior

`bg-rose-500/10 text-rose-400` on every page where the Video badge appears.

### Actual behavior

```
Card view:    bg-rose-500/10 text-rose-400  ✓
List view:    bg-red-500/10 text-red-400    ✗
Detail page:  bg-red-500/10 text-red-400    ✗
```

### Root cause

The `content_list.html` list-mode badge block and `content_detail.html` badge block were originally authored with Tailwind `red` (visually close to `rose` but a distinct palette). The Sprint 4 fix targeted only the dashboard. Sprint 5 introduced `content_card.html` with the correct `rose` token. Sprint 6's design consistency audit did not catch the residual `red` occurrences in the list and detail templates.

### Fix applied

**`templates/contents/content_detail.html`** — line 40:
```
bg-red-500/10 text-red-400  →  bg-rose-500/10 text-rose-400
```

**`templates/contents/content_list.html`** — all occurrences (replace_all):
```
bg-red-500/10 text-red-400  →  bg-rose-500/10 text-rose-400
```

### Impact

Visual inconsistency: the same "Video" status rendered with different shades depending on which view the user was on. This undermines the design system's color language and creates a perception of a buggy or unpolished product.

---

## Fix Summary

| ID | Modified file | Change | Migration needed |
|----|--------------|--------|-----------------|
| B-01 | `templates/contents/content_list.html` | `getElementById('view-cards')` → `getElementById('view-cards-container')` and same for `view-list` | No |
| B-02 | `templates/contents/content_detail.html` | `bg-red-500/10 text-red-400` → `bg-rose-500/10 text-rose-400` on Video badge | No |
| B-02 | `templates/contents/content_list.html` | `bg-red-500/10 text-red-400` → `bg-rose-500/10 text-rose-400` (all occurrences) | No |
