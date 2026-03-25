---
name: Sprint 5 AI Insights
description: AI Insights backend — AIService, rate limiting, and three JSON API views in the insights app
type: project
---

Sprint 5 implemented the AI backend for the `insights` app.

**Why:** Adds Claude-powered suggestions (category, description, usage insights) as user-triggered JSON endpoints consumed by the frontend via fetch/HTMX.

**How to apply:** When extending AI features, follow the pattern in `insights/services.py` — all Anthropic calls are wrapped in granular except blocks, and `check_rate_limit` (session-based) gates each endpoint.

Key decisions:
- `anthropic==0.86.0` added to `requirements.txt`; `ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')` added near the bottom of `core/settings.py`
- `insights` app and `insights/` URL prefix were already registered in Sprint 1 — no changes needed to `INSTALLED_APPS` or `core/urls.py`
- `DashboardService(user=request.user).get_stats()` is the source of data for `GenerateInsightsView`
- Rate limits: `suggest_category` and `generate_description` → 10 calls/hour; `generate_insights` → 5 calls/hour
- No models and no migrations in the `insights` app (by design)
