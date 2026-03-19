# Code Standards

## Python / Django

- **Style:** PEP 8 compliance
- **Quotes:** Single quotes `'`
- **Language:** All code, variable names, comments, and docstrings in English
- **Views:** Class-Based Views (CBVs) as the primary pattern — no function-based views unless strictly necessary
- **Auth protection:** All authenticated views must use `LoginRequiredMixin`

## Models

- Every model must define `created_at` and `updated_at` fields:

```python
from django.db import models

class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- Models go in `models.py` inside their respective app
- User-scoped models (categories, tags, contents) must have a `ForeignKey` to the custom user model

## App Structure

Each app follows this layout:

```
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

## URLs

- Each app defines its own `urls.py`
- All app URLs are included in `core/urls.py` using `include()`
- URL names follow the pattern `app_name:action` (e.g., `contents:list`, `contents:create`)

## Templates

- All templates live in a top-level `templates/` directory
- Authenticated pages extend `base.html`
- Public pages (landing, login, register) extend `base_public.html`
- Template names follow the pattern `app_name/template_name.html`

## Forms

- Forms are defined in `forms.py` within each app
- Use `ModelForm` where appropriate
- Validation errors are rendered inline in templates

## Security

- CSRF protection is enabled on all POST forms via `{% csrf_token %}`
- Passwords are hashed using Django's built-in password hashers
- File uploads are validated server-side:
  - Allowed extensions: PDF, JPG, JPEG, PNG, GIF, WebP, MP3, MP4, DOC, DOCX, TXT, MD
  - Maximum size: 10 MB
  - Uploads are stored outside the static directory
- URL fetching (Open Graph): validate against private/internal IPs, enforce timeout (5s), limit response size

## AI Features

- AI calls use the Anthropic Claude API via the `anthropic` Python SDK
- AI features are **always user-triggered** (button click) — never automatic
- The app must remain fully functional when the AI service is unavailable
- Errors from the AI service must be handled gracefully with user-facing messages

## File and Folder Naming

- Python files: `snake_case.py`
- Template files: `snake_case.html`
- Django app folders: `snake_case/`

## Dependencies

Defined in `requirements.txt`. Add new packages only when they are needed for an existing feature.
