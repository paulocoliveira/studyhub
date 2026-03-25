---
name: Sprint 8 API Key Settings
description: Per-user AI provider and API key storage; AIService refactored to support both Anthropic and OpenAI from user model
type: project
---

CustomUser gained two fields: `ai_provider` (CharField, choices anthropic/openai, default anthropic) and `ai_api_key` (CharField max 200, blank=True).

**Why:** Users should be able to supply their own API keys so AI features work without server-side env vars.

**How to apply:** AIService.__init__ now accepts `user=` and reads key/provider from user model, falling back to settings.ANTHROPIC_API_KEY when blank. All three insights views pass `user=request.user`. UserSettingsForm.clean_ai_api_key preserves existing key when field submitted blank (PasswordInput doesn't pre-fill). openai==2.29.0 added to requirements.txt. Migration: users/migrations/0002_customuser_ai_api_key_customuser_ai_provider.py.
