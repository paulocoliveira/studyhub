---
name: Sprint 6 template structure
description: Polish & Refinements — responsive layout, empty states, flash auto-dismiss, breadcrumbs, URL auto-detect
type: project
---

Sprint 6 (Polish & Refinements) implemented 2026-03-25.

## 6.1 Responsive Design

**Why:** Sidebar used `lg:` breakpoint instead of spec-required `md:` breakpoint.

Changed in `templates/base.html`:
- Sidebar visible wrapper: `hidden md:flex md:flex-col md:shrink-0`
- Mobile overlay: `hidden md:hidden`
- Mobile drawer: `-translate-x-full md:hidden`
- Hamburger button: `md:hidden`
- Added `DOMContentLoaded` listener to close mobile sidebar when any `<a>` in `#mobile-sidebar` is clicked.

**How to apply:** Always use `md:` as the sidebar breakpoint. Desktop = md+, mobile = below md.

## 6.2 Empty States

All list pages already had solid empty states from prior sprints. No changes needed for content_list, category_list, tag_list.

**Dashboard onboarding (6.2.4):** Added `{% if stats.total_contents == 0 %}` section before the stats row in `templates/dashboard/dashboard.html`. Shows a gradient card with 3 quick-start action cards (Add Content, Create Category, Create Tag) using group hover colors (violet/emerald/amber).

## 6.3 Flash Messages

**Auto-dismiss (6.3.2):** Added `data-message` attribute to each `[role=alert]` div in `templates/components/messages.html`. Added inline `<script>` after the message loop that uses `setTimeout` to fade opacity to 0 then removes the element after 5.5s total (5s delay + 0.5s fade).

## 6.4 Navigation

**Breadcrumbs (6.4.2):** Created `templates/components/breadcrumbs.html` as a reusable component (takes `breadcrumbs` context list).

Breadcrumbs hardcoded inline (no view changes needed) in:
- `content_detail.html`: Contents / {content.title}
- `content_form.html`: Contents / {title} / Edit OR Contents / Create (uses `form.instance.pk`)
- `category_form.html`: Categories / Edit OR Categories / Create
- `tag_form.html`: Tags / Create

**Back links (6.4.3):** All form and detail pages already had back links from prior sprints — no changes needed.

**Sidebar active state (6.4.1):** Path slice checks verified correct:
- `/contents` = slice `:9` ✓
- `/categories` = slice `:11` ✓
- `/tags` = slice `:5` ✓
- `/insights` = slice `:9` ✓
- dashboard uses exact `request.path == dashboard_url` ✓

## 6.5 Content Form UX

**Tag picker (6.5.1):** Already implemented via `group-has-[:checked]:` pattern from Sprint 3/4 — checkbox iteration with hidden native checkboxes styled as pills.

**Client-side validation (6.5.2):** Form already has `novalidate` from prior sprint. Django server-side errors render via `{{ form.field.errors }}`.

**URL auto-detect (6.5.3):** Added IIFE in `{% block scripts %}` of `content_form.html`. Fires on `blur` of `#id_url`. Only sets `id_content_type` if current value matches the first/default option. Patterns: YouTube→video, Spotify→podcast, Instagram/Twitter/X/TikTok→social_media_post, Amazon books/Goodreads→book, Udemy/Coursera/edX/Pluralsight→course.

## 6.6 Design Consistency

All existing templates already used correct design system tokens from prior sprints. No color/button/badge inconsistencies found.
