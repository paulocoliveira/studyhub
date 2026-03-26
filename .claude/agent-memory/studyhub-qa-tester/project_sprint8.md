---
name: Sprint 8 QA findings
description: QA results for Sprint 8 (Advanced AI & Learning Intelligence): 3 bugs found, 23/28 pass
type: project
---

## Sprint 8 QA — Advanced AI & Learning Intelligence (2026-03-26)

Static analysis only (no server required per task spec).

### Bugs found

- **BUG-01 Medium:** Self-XSS in forgotten content list — `item.title` from JSON response inserted into `innerHTML` without escaping in `templates/insights/index.html` lines 335-340. The `escapeHtml` helper IS already defined in the same script; just not used here. Fix: wrap `item.title` with `escapeHtml()`.
- **BUG-02 Low:** `_render_markdown` in `insights/views.py` wraps numbered list items in `<ol>` (line 23) but NEVER wraps bullet list items in `<ul>` (step at line 25-26 is missing). Output is bare `<li>` inside `<p>` — invalid HTML5.
- **BUG-03 Low:** `_render_markdown` `<ol>` wrapping uses greedy `re.DOTALL` regex that absorbs non-list content between numbered items. Produces structurally broken `<ol>` when list items are separated by blank-line paragraphs.

### What passed

- All 5 new views (`SuggestNextView`, `ForgottenContentsView`, `AnalyzeTopicsView`, `WeeklySummaryView`, `ChatView`) have `LoginRequiredMixin`.
- All 5 new URL patterns registered in `insights/urls.py`.
- `build_user_context` is module-level with lazy model imports inside function body (correct circular-import avoidance).
- `DashboardService.get_forgotten_contents` filters `status='new'` and `created_at__lte=cutoff` correctly.
- `ChatView` history handling: `chatHistory.slice(0, -1)` correctly excludes current user message from history param; `AIService.chat()` appends it server-side. No duplication.
- `_render_markdown` escapes HTML first via `html.escape()` — AI output XSS is safe.
- Chat assistant messages: client-side `escapeHtml()` runs on AI reply before bold/br substitution — safe.
- `DOMContentLoaded` timing: event fires AFTER bottom-of-body inline scripts, so forgotten content auto-load works.
- Django system check: 0 issues.
- OpenAI SDK v2 API pattern (`client.chat.completions.create`) used correctly.

### Recurring patterns

- Zero automated test coverage in all tests.py files (same as every prior sprint).
- Self-XSS via innerHTML concatenation is a new pattern (not seen in previous sprints).
- `_render_markdown` is new in Sprint 8 and has two rendering bugs (BUG-02, BUG-03).

### Warnings

- `AIService.ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001'` — non-standard model ID format. Verify against Anthropic model catalog at runtime.
- Non-primary button gradients (`sky`, `violet`) used for themed AI cards — outside design system primary spec but contextually reasonable. Flag for design team.
