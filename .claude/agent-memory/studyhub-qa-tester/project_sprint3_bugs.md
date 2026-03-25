---
name: Sprint 3 known bugs
description: Bugs discovered during Sprint 3 QA — search param mismatch (High), badge color drift (Medium), delete button style (Low)
type: project
---

Three bugs found during Sprint 3 QA (2026-03-25):

**BUG-01 (High) — Search filter broken in UI**
`ContentFilterForm` field is named `search` (submits `?search=`), but `ContentListView.get_queryset()` reads `request.GET.get('q', '')`. The search box in the browser does nothing. Fix: rename the form field to `q`, or change the view to read `search`.
Affects: `contents/forms.py` line 56, `contents/views.py` line 30.

**BUG-02 (Medium) — Status badge color palette deviation**
Templates use `blue`/`yellow`/`green` Tailwind classes for status badges. Design system specifies `sky`/`amber`/`emerald`.
Affects: `templates/contents/content_list.html`, `templates/contents/content_detail.html`.

**BUG-03 (Low) — Delete confirm button uses solid red, not design system danger style**
`content_confirm_delete.html` uses `bg-red-600 hover:bg-red-700`. Design system specifies translucent rose: `bg-rose-600/10 text-rose-500 border border-rose-500/20 hover:bg-rose-600/20`.
Affects: `templates/contents/content_confirm_delete.html`.

**Why to apply:** When reviewing future PRs or sprint work touching content templates or the content list view, check whether these bugs have been fixed first before testing related behavior.
