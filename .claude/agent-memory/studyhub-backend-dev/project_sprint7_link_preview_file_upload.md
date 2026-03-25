---
name: Sprint 7 Link Preview and File Upload
description: Sprint 7 added link preview metadata extraction, auto-fetch OG signal, file upload field, and get_card_image() to the Content model
type: project
---

Sprint 7 implemented link preview and file upload features for the `contents` app.

**Why:** To enrich content cards with OG images and allow users to attach files to their content entries.

**How to apply:** When working in `contents`, these new fields and helpers are available:

- `Content.preview_image_url` — URLField(max_length=500, blank=True) storing fetched OG image URL
- `Content.file` — FileField(upload_to='content_files/%Y/%m/', blank=True, null=True) with validators
- `Content.get_card_image()` — model method with priority: uploaded image > OG preview > static placeholder SVG

New files created:
- `contents/services.py` — `LinkPreviewService` class with `fetch_preview(url)` and `_is_safe_url(url)`
- `contents/validators.py` — `validate_file_extension` and `validate_file_size` functions
- `contents/signals.py` — `pre_save` signal on Content that auto-fetches OG image when URL is set/changed and preview_image_url is empty

New view: `RefreshPreviewView` (POST `<int:pk>/refresh-preview/`, name `contents:refresh_preview`) — JSON API to manually re-fetch OG preview for a content item.

Settings added to `core/settings.py`: `ALLOWED_UPLOAD_EXTENSIONS`, `MAX_UPLOAD_SIZE_MB`, fixed `MEDIA_URL` to `/media/` (was `media/`).

`core/urls.py` now serves media files via `static(settings.MEDIA_URL, ...)` in development.

`requirements.txt` now includes `requests==2.33.0` and `beautifulsoup4==4.14.3`.

Migration: `contents/migrations/0002_content_file_content_preview_image_url.py`
