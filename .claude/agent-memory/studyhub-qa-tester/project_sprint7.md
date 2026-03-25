---
name: Sprint 7 QA findings
description: Sprint 7 (Content Cards, Link Previews & File Upload) QA results — 22 pass, 2 fail, 1 warn; view toggle broken by ID mismatch; red/rose video badge regression persists
type: project
---

## Sprint 7 QA — 2026-03-25

**Result:** 22 PASS / 2 FAIL / 1 WARN out of 25 TCs.

### BUG-01 (High) — View toggle non-functional: JS/HTML element ID mismatch
`content_list.html` JS references `getElementById('view-cards')` and `getElementById('view-list')` but HTML container divs have IDs `view-cards-container` and `view-list-container`. Both `cardView`/`listView` vars are null, so `applyView()` is a no-op. Both card grid and list view are simultaneously visible on every page load; toggle buttons have no effect on container visibility. Button active-state styling works correctly (those targets btn-view-cards/btn-view-list which are correct).

Fix: Line 295 `getElementById('view-cards')` → `getElementById('view-cards-container')`. Line 296 `getElementById('view-list')` → `getElementById('view-list-container')`.

### BUG-02 (Medium) — Video type badge uses red instead of rose (persists Sprint 4/6)
`content_detail.html` (line 40) and `content_list.html` list view (line 154) use `bg-red-500/10 text-red-400`. Design system requires `bg-rose-500/10 text-rose-400`. `content_card.html` was correctly updated to `rose` in Sprint 7, creating a 3-way inconsistency.

### WARN-01 — Video badge partially fixed in Sprint 7
Card component now uses rose correctly; detail and list views still use red. Same bug from Sprint 4 remains in 2 of 3 locations.

### What passed cleanly
- Django system check: 0 issues
- All migrations applied
- Content model has `preview_image_url` and `file` fields
- LinkPreviewService: SSRF protection working (empty string, private IP 192.168.x.x, loopback 127.0.0.1)
- validate_file_extension: rejects .exe, allows pdf/jpg/png/mp3/docx/md
- validate_file_size: rejects 11MB file with clear error message
- get_card_image(): returns placeholder path (article.svg) when no file/preview; returns preview_image_url when set
- Signal registered (ContentsConfig.ready)
- RefreshPreviewView: rejects unauthenticated (302 to login), rejects wrong user (404)
- Content create form: 200, id_file present, enctype multipart/form-data
- Content list: 200, btn-view-cards and btn-view-list present
- content_card.html: get_card_image, onerror fallback, line-clamp-2, type + status badge overlays all correct
- All 7 placeholder SVGs exist: article, video, podcast, course, book, tool, other
- MEDIA_URL=/media/, MEDIA_ROOT contains 'media'
- File upload field: enctype, form.file, helper text, id_file JS change listener all present
- Refresh preview button: inside correct conditional, data-url, JS fetch handler
- Download link in detail: if content.file block, download attr, content.file.url
- File upload functional: POST with valid PDF → 302
- .exe file rejection (server-side): POST with .exe → 200 with error message
- ALLOWED_UPLOAD_EXTENSIONS list present; MAX_UPLOAD_SIZE_MB == 10
