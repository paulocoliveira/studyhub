# StudyHub

A personal knowledge management tool to organize and track your learning content.

## Features

- **Contents management** — save articles, videos, books, courses, and more with full CRUD, file upload, and Open Graph preview image fetching
- **Categories** — user-scoped categories to group related content
- **Tags** — flexible tagging system for cross-category organization
- **AI-powered insights** — Claude-backed category suggestions, description generation, topic analysis, weekly summaries, and a chat assistant
- **Dashboard with stats** — at-a-glance view of content by status and type, top categories, top tags, and forgotten content reminders

## Tech Stack

- Python 3.13 / Django 6
- TailwindCSS (via CDN)
- SQLite 3
- Anthropic Claude API
- Docker / Gunicorn / Whitenoise

## Local Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd studyhub

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the example env file and fill in your values
cp .env.example .env

# 5. Apply database migrations
python manage.py migrate

# 6. Create an admin superuser (optional)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Open http://localhost:8000 in your browser.

## Docker Setup

```bash
# 1. Copy the example env file and fill in your values
cp .env.example .env

# 2. Build and start the container
docker-compose up --build
```

The application will be available at http://localhost:8000.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | insecure dev fallback | Django secret key — use a long random string in production |
| `DEBUG` | No | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated list of allowed hostnames |
| `ANTHROPIC_API_KEY` | No | _(empty)_ | API key for Anthropic Claude — AI features are disabled without it |

## Screenshots

_Coming soon._
