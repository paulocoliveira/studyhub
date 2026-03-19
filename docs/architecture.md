# Architecture

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13+ |
| Framework | Django 6.x |
| Database | SQLite 3 (Django default) |
| Frontend | Django Template Language (DTL) |
| CSS | TailwindCSS (via CDN) |
| AI | Anthropic Claude API (`anthropic` SDK) |
| Auth | Django native auth with custom User model |
| Link Preview | `requests` + `beautifulsoup4` (Open Graph extraction) |
| File Storage | Django `FileField` with local media storage |

## Django Apps

| App | Responsibility |
|---|---|
| `core` | Project settings, root URL configuration, base templates, static files |
| `users` | Custom user model (email-based login), registration, authentication views |
| `contents` | Content CRUD, filtering, search, status management |
| `categories` | Category CRUD, user-scoped management |
| `tags` | Tag CRUD, user-scoped management |
| `insights` | AI service integration, insight generation views |
| `dashboard` | Aggregated statistics and overview views |

## URL Structure

Each app owns its own `urls.py` and is included from `core/urls.py`:

```
/                       → landing page (users app)
/register/              → user registration
/login/                 → login
/logout/                → logout
/password/change/       → password change
/dashboard/             → main dashboard
/contents/              → content list
/contents/add/          → add content
/contents/<id>/         → content detail
/contents/<id>/edit/    → edit content
/contents/<id>/delete/  → delete content
/categories/            → category list
/tags/                  → tag list
/insights/              → AI insights
```

## Settings Overview

Key settings defined in `core/settings.py`:

- `AUTH_USER_MODEL = 'users.CustomUser'` — custom user model
- `LANGUAGE_CODE = 'en-us'`
- `TIME_ZONE = 'UTC'`
- `MEDIA_URL` and `MEDIA_ROOT` — for user file uploads
- `LOGIN_URL`, `LOGIN_REDIRECT_URL` — auth redirect configuration
- All apps listed in `INSTALLED_APPS`

## Authentication

- Login credential: **email** (not username)
- Custom user model extends `AbstractBaseUser`
- Django's built-in CSRF, session, and password hashing are used
- All authenticated views require `LoginRequiredMixin`
