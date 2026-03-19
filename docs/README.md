# StudyHub — Documentation

> Personal learning content management system built with Python, Django, SQLite, and TailwindCSS.

## Index

| Document | Description |
|---|---|
| [Architecture](./architecture.md) | Tech stack, Django apps, project configuration |
| [Data Schema](./data-schema.md) | Models, fields, and relationships |
| [Design System](./design-system.md) | Color palette, typography, and UI components |
| [Code Standards](./code-standards.md) | Conventions, patterns, and project rules |

## Quick Start

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Project Structure

```
studyhub/
├── core/           # Settings, root URLs
├── users/          # Authentication and user model
├── contents/       # Content CRUD
├── categories/     # Category management
├── tags/           # Tag management
├── dashboard/      # Aggregated stats view
├── insights/       # AI feature integration
├── aireports/      # QA bug and test report templates
├── docs/           # This documentation
├── PRD.md          # Full product requirements
├── TASKS.md        # Sprint-based task breakdown
└── requirements.txt
```
