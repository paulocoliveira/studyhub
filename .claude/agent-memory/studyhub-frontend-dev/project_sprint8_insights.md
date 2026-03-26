---
name: Sprint 8 Insights page redesign
description: Full rewrite of templates/insights/index.html — two-column layout, five AI cards, AI chat panel, vanilla JS AJAX wiring
type: project
---

The Insights page (`templates/insights/index.html`) was completely rewritten in Sprint 8.

**Layout:** `lg:grid-cols-12` two-column grid. Left column (`lg:col-span-7`) holds five stacked AI cards. Right column (`lg:col-span-5`) holds a sticky AI chat panel (`lg:sticky lg:top-20`). Single column on mobile with left cards first, chat below.

**Left column cards (top to bottom):**
1. Forgotten Content — auto-loaded on `DOMContentLoaded` via `GET /insights/forgotten-contents/`. Shows amber icon, list of items with type badges, or empty state.
2. What to Study Next — button-triggered, `POST /insights/suggest-next/`, green accent.
3. Consumption Insights — button-triggered, `GET /insights/generate-insights/` (returns `{success, insights}` not `{success, html}` — JS wraps it in `<p>`), sky/blue accent.
4. Topic Patterns — button-triggered, `POST /insights/analyze-topics/`, violet accent.
5. Weekly Summary — button-triggered, `POST /insights/weekly-summary/`, result wrapped in `<blockquote>` with emerald border, emerald accent.

**AI Chat panel:**
- `#chat-messages`: flex-col scrollable, `flex-1 overflow-y-auto min-h-0`
- User bubbles: right-aligned, `bg-green-500/10 border-green-500/20 rounded-xl rounded-tr-sm`
- Assistant bubbles: left-aligned with avatar, `bg-zinc-800 rounded-xl rounded-tl-sm`
- Typing indicator: three bouncing dots with staggered `animation-delay`
- Starter chips: `#chat-chips`, hidden after first message sent, restored on "New chat"
- History: JS array `chatHistory`, never persisted to DB
- Send: button click or `Enter` (without Shift); `Shift+Enter` = newline

**Key JS patterns:**
- `setupAiCard(btnId, loadingId, placeholderId, resultId, errorId, fetchFn)` — reusable helper for all button-triggered cards
- CSRF read order: `[name=csrfmiddlewaretoken]` first, then cookie fallback (`/csrftoken=([^;]+)/`)
- All API calls use `postJson()` or `getJson()` helpers
- Markdown rendering: `**bold**` → `<strong>`, `\n` → `<br>` (in chat replies only)
- Content type badge colors: violet=article, rose=video, orange=podcast, cyan=course, emerald=book, pink=tool, zinc=other

**Why:** Consolidates all Sprint 8 AI features (tasks 8.1.4, 8.2.4, 8.3.4, 8.4.4, 8.5.5–8.5.7, 8.6.1–8.6.3) into a single redesigned page.

**How to apply:** When touching the Insights page in future sprints, preserve the two-column grid structure and the `setupAiCard` helper pattern. The generate-insights endpoint is a GET that returns `{insights}` not `{html}` — handle this specially.
