# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (always required)
source .venv/bin/activate

# Run development server
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test contents
python manage.py test users

# Run a single test case
python manage.py test contents.tests.ContentModelTest.test_default_status

# Open Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```

## Architecture

Django full-stack monolith. No separate frontend framework — all rendering is done server-side via Django Template Language (DTL) with TailwindCSS via CDN.

### Apps and their responsibilities

| App | Purpose |
|---|---|
| `core` | Settings (`core/settings.py`), root URL config (`core/urls.py`) |
| `users` | Custom user model (email-based login), registration, auth views |
| `contents` | Content CRUD, filtering, search, status management |
| `categories` | Category CRUD, user-scoped |
| `tags` | Tag CRUD, user-scoped |
| `dashboard` | Aggregated stats view — reads from other apps, owns no models |
| `insights` | AI feature views (Claude API integration) — owns no models |

Each app owns its own `models.py`, `views.py`, `forms.py`, `urls.py`, and `admin.py`. App URLs are included from `core/urls.py`.

### Authentication

- Login credential is **email**, not username
- Custom user model must be set as `AUTH_USER_MODEL = 'users.CustomUser'` in settings
- All authenticated views use `LoginRequiredMixin`

### Templates

- Authenticated pages extend `base.html`
- Public pages (landing, login, register) extend `base_public.html`
- Template files live under `templates/` at the project root or inside each app's `templates/app_name/` folder

### Data ownership

Categories and tags are **user-scoped** — always filter querysets by `user=request.user`. Contents belong to a user; deleting a category sets `content.category` to `null` (no cascade).

### AI features (`insights` app)

Uses the Anthropic Claude API via the `anthropic` Python SDK. AI calls are always **user-triggered** — never automatic. The app must work fully when the AI service is unavailable; handle API errors gracefully.

### File uploads

`Content` has an optional `FileField`. Allowed extensions: PDF, JPG, JPEG, PNG, GIF, WebP, MP3, MP4, DOC, DOCX, TXT, MD. Max size: 10 MB. Validate server-side. Store uploads outside the static directory via `MEDIA_ROOT`.

### Open Graph preview images

When a content URL is saved, fetch its Open Graph image using `requests` + `beautifulsoup4` and store it in `Content.preview_image_url`. Validate the URL before fetching: reject private/internal IPs, set a 5-second timeout, limit response size. Never fetch automatically on every request — only on content save.

## Code Conventions

- **Views:** Class-Based Views only (`ListView`, `CreateView`, `UpdateView`, `DeleteView`, `DetailView`, `TemplateView`)
- **Quotes:** single quotes `'`
- **Models:** every model must have `created_at = DateTimeField(auto_now_add=True)` and `updated_at = DateTimeField(auto_now=True)`
- **URL names:** `app_name:action` pattern (e.g. `contents:list`, `contents:create`)
- All code and comments in English

## Documentation

- `PRD.md` — full product requirements, functional specs, user stories, and design system reference
- `docs/` — distilled guidelines: architecture, data schema, design system, code standards
