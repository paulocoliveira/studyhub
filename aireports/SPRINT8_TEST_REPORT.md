## Test Report — Sprint 8: Advanced AI & Learning Intelligence
**Date:** 2026-03-26
**Tester:** QA Agent
**Method:** Static analysis (source code review + Django system check + logic verification)
**Server:** Not required — static analysis only

---

### Summary

| Total | Passed | Failed | Warnings |
|---|---|---|---|
| 28 | 23 | 3 | 2 |

---

### Test Cases

#### TC-01 — Django system check
- **Pre-condition:** Virtual environment activated, all migrations applied
- **Steps:** `python manage.py check 2>&1`
- **Expected:** Zero issues reported
- **Actual:** "System check identified no issues (0 silenced)."
- **Status:** PASS

---

#### TC-02 — Test suite execution
- **Pre-condition:** Virtual environment activated
- **Steps:** `python manage.py test --verbosity=2 2>&1`
- **Expected:** All tests pass
- **Actual:** "Ran 0 tests in 0.000s / NO TESTS RAN" — all `tests.py` files across all apps are empty stubs
- **Status:** WARN
- **Note:** `insights/tests.py`, `dashboard/tests.py`, `contents/tests.py`, `categories/tests.py`, `tags/tests.py`, and `users/tests.py` all contain only stub comments. No automated test coverage exists for any Sprint 8 feature.

---

#### TC-03 — `build_user_context` module-level function exists in `insights/services.py`
- **Pre-condition:** Read `insights/services.py`
- **Steps:** Verify function signature and location
- **Expected:** Module-level function `build_user_context(user)` exists
- **Actual:** Defined at line 8, module-level, correct signature
- **Status:** PASS

---

#### TC-04 — `build_user_context` avoids circular imports
- **Pre-condition:** Read `insights/services.py` lines 12-15
- **Steps:** Verify all model imports are inside the function body
- **Expected:** `from contents.models import Content`, `from categories.models import Category`, `from tags.models import Tag` all inside function body
- **Actual:** All three model imports are deferred inside the function body (lines 12-15). CORRECT.
- **Status:** PASS

---

#### TC-05 — `AIService` methods: `suggest_next`, `analyze_topics`, `weekly_summary`, `chat`, `_call_ai_messages`
- **Pre-condition:** Read `insights/services.py`
- **Steps:** Verify each method exists on `AIService` class
- **Expected:** All 5 methods present
- **Actual:**
  - `suggest_next(self, user)` — line 182. PRESENT.
  - `analyze_topics(self, user)` — line 214. PRESENT.
  - `weekly_summary(self, user)` — line 245. PRESENT.
  - `chat(self, user, message, history)` — line 278. PRESENT.
  - `_call_ai_messages(self, messages, system_prompt, max_tokens)` — line 154. PRESENT.
- **Status:** PASS

---

#### TC-06 — `DashboardService.get_forgotten_contents` query correctness
- **Pre-condition:** Read `dashboard/services.py`
- **Steps:** Verify method signature, filter conditions, and ordering
- **Expected:** Filters `status='new'` and `created_at__lte=cutoff` where `cutoff = now - timedelta(days=days)`
- **Actual:** Lines 71-79 confirm: `cutoff = timezone.now() - timedelta(days=days)`, `.filter(user=self.user, status='new', created_at__lte=cutoff)`, `.order_by('created_at')[:10]`. All correct.
- **Status:** PASS

---

#### TC-07 — All 5 new views present in `insights/views.py` with `LoginRequiredMixin`
- **Pre-condition:** Read `insights/views.py`
- **Steps:** Verify class definitions and inheritance
- **Expected:** All 5 new views inherit from `LoginRequiredMixin` and `View`
- **Actual:**
  - `SuggestNextView(LoginRequiredMixin, View)` — line 146. PRESENT.
  - `ForgottenContentsView(LoginRequiredMixin, View)` — line 165. PRESENT.
  - `AnalyzeTopicsView(LoginRequiredMixin, View)` — line 186. PRESENT.
  - `WeeklySummaryView(LoginRequiredMixin, View)` — line 205. PRESENT.
  - `ChatView(LoginRequiredMixin, View)` — line 224. PRESENT.
- **Status:** PASS

---

#### TC-08 — All 5 new URL patterns registered in `insights/urls.py`
- **Pre-condition:** Read `insights/urls.py`
- **Steps:** Verify each path entry
- **Expected:** `suggest-next/`, `forgotten-contents/`, `analyze-topics/`, `weekly-summary/`, `chat/` all registered
- **Actual:** Lines 12-16 confirm all 5 paths are registered with correct view names
- **Status:** PASS

---

#### TC-09 — `ForgottenContentsView.get` returns correct JSON structure
- **Pre-condition:** Read `insights/views.py` lines 165-183
- **Steps:** Trace the response structure
- **Expected:** Returns `{'success': True, 'items': [...]}` with each item having `id`, `title`, `content_type`, `days_since_saved`, `detail_url`
- **Actual:** Lines 170-180 build the exact expected structure. `detail_url` uses `f'/contents/{item.pk}/'` (integer pk, no XSS risk from this field).
- **Status:** PASS

---

#### TC-10 — `ChatView.post` JSON body validation
- **Pre-condition:** Read `insights/views.py` lines 227-261
- **Steps:** Trace validation logic
- **Expected:** Validates JSON parse, requires non-empty `message`, sanitizes `history` list
- **Actual:**
  - JSON parse error returns 400. CORRECT.
  - Empty message returns 400. CORRECT.
  - `history` validated as list with role in ('user', 'assistant') and non-empty content. CORRECT.
- **Status:** PASS

---

#### TC-11 — `ChatView` history parameter: current message not duplicated in history
- **Pre-condition:** Read JS in `templates/insights/index.html` lines 496-505
- **Steps:** Trace how `chatHistory` and the fetch body are constructed
- **Expected:** Current message should not appear in both the `message` field and the `history` field sent to the server
- **Actual:**
  - Line 496: `chatHistory.push({ role: 'user', content: text })` (pushes current message)
  - Line 505: `postJson('/insights/chat/', { message: text, history: chatHistory.slice(0, -1) })` (slice removes last item = current message)
  - Server `AIService.chat()` line 291: `messages = list(history) + [{'role': 'user', 'content': message}]` (appends current message)
  - CORRECT: no duplication.
- **Status:** PASS

---

#### TC-12 — `_render_markdown` HTML escaping (XSS prevention from AI output)
- **Pre-condition:** Read `insights/views.py` lines 15-29; run manual test
- **Steps:** Pass `<script>alert(1)</script>` through `_render_markdown`
- **Expected:** HTML entities escaped; no executable script tags in output
- **Actual:** `html.escape(text)` runs first (line 18), producing `&lt;script&gt;alert(1)&lt;/script&gt;`. Output is safe.
- **Status:** PASS

---

#### TC-13 — Chat assistant messages XSS safety
- **Pre-condition:** Read JS lines 511-518 in `templates/insights/index.html`
- **Steps:** Trace AI reply rendering path
- **Expected:** AI reply content escaped before being set as innerHTML
- **Actual:** Line 514: `escapeHtml(reply)` runs before bold/newline substitutions. The bold regex `<strong>` tags are safe since the content between them was already escaped. SAFE.
- **Status:** PASS

---

#### TC-14 — Forgotten content list: XSS risk from `item.title` in innerHTML
- **Pre-condition:** Read JS lines 332-343 in `templates/insights/index.html`
- **Steps:** Trace how `item.title` from server JSON is inserted into DOM
- **Expected:** Title should be escaped before being inserted into innerHTML
- **Actual:** `item.title` is inserted directly into innerHTML string concatenation at line 337 (`<a ... title="' + item.title + '">'  + item.title + '</a>'`) without any escaping. A title such as `"><script>alert(1)</script>` would break HTML structure. This is a self-XSS vulnerability (user can only exploit their own session since data is user-scoped), but still violates safe coding practice.
- **Status:** FAIL
- **See:** BUG-01

---

#### TC-15 — `_render_markdown` bullet list `<ul>` wrapper
- **Pre-condition:** Read `insights/views.py` lines 25-26; run manual test
- **Steps:** Pass `'- Bullet A\n- Bullet B\n- Bullet C'` through `_render_markdown`
- **Expected:** Bullet items wrapped in `<ul>`
- **Actual:** Bullet items converted to `<li>` tags (line 25) but no `<ul>` wrapping step exists. Output: `<p><li>Bullet A</li><br><li>Bullet B</li><br><li>Bullet C</li></p>` — invalid HTML5 (bare `<li>` inside `<p>`).
- **Status:** FAIL
- **See:** BUG-02

---

#### TC-16 — `generate-insights` endpoint still functional (GET method)
- **Pre-condition:** Read `insights/views.py` line 121; read `insights/urls.py` line 11
- **Steps:** Verify HTTP method and URL registration
- **Expected:** `GenerateInsightsView` uses GET; URL `generate-insights/` registered
- **Actual:** `def get(self, request, ...)` at line 121. URL registered at line 11 of urls.py. CORRECT.
- **Status:** PASS

---

#### TC-17 — `generate-insights` JS response handling (GET fetch, `insights` vs `html` field)
- **Pre-condition:** Read JS lines 392-405 in `templates/insights/index.html`
- **Steps:** Trace how the generate-insights JS handles the `{success, insights}` response format
- **Expected:** Response field `insights` (string) converted to `html` before `setupAiCard` reads `data.html`
- **Actual:** Lines 399-401: on success, `d.html` is constructed from `d.insights` with basic bold rendering. Then `setupAiCard` reads `data.html || data.insights`. The conversion is correct. PASS.
- **Status:** PASS

---

#### TC-18 — Two-column layout in `templates/insights/index.html`
- **Pre-condition:** Read `templates/insights/index.html` lines 19-20
- **Steps:** Verify grid class
- **Expected:** `lg:grid-cols-12` present with 7-col left + 5-col right split
- **Actual:** Line 19: `class='grid grid-cols-1 lg:grid-cols-12 gap-6'`. Left: `lg:col-span-7`. Right: `lg:col-span-5`. CORRECT.
- **Status:** PASS

---

#### TC-19 — All required element IDs present in template
- **Pre-condition:** Read `templates/insights/index.html`
- **Steps:** Verify IDs `btn-suggest-next`, `btn-generate-insights`, `btn-analyze-topics`, `btn-weekly-summary`, `chat-messages`, `chat-input`, `btn-chat-send`, `btn-new-chat`
- **Expected:** All 8 IDs present
- **Actual:**
  - `btn-suggest-next` — line 63. PRESENT.
  - `btn-generate-insights` — line 97. PRESENT.
  - `btn-analyze-topics` — line 131. PRESENT.
  - `btn-weekly-summary` — line 165. PRESENT.
  - `chat-messages` — line 214. PRESENT.
  - `chat-input` — line 254. PRESENT.
  - `btn-chat-send` — line 259. PRESENT.
  - `btn-new-chat` — line 206. PRESENT.
- **Status:** PASS

---

#### TC-20 — Chat starter chips with `data-chip` attributes
- **Pre-condition:** Read `templates/insights/index.html` lines 232-248
- **Steps:** Verify chips have `data-chip` attributes and click handler reads `dataset.chip`
- **Expected:** All chips have `data-chip` attribute; JS reads `this.dataset.chip`
- **Actual:** 4 chip buttons with `data-chip` attributes at lines 232-247. JS line 548: `sendMessage(this.dataset.chip)`. CORRECT.
- **Status:** PASS

---

#### TC-21 — Forgotten content auto-load on `DOMContentLoaded`
- **Pre-condition:** Read template JS lines 566-569; read `base.html` line 77
- **Steps:** Verify timing of `DOMContentLoaded` vs script execution
- **Expected:** `loadForgottenContent()` called on page load
- **Actual:** The `{% block scripts %}` is placed at line 77 of `base.html`, at the end of `<body>` but before `</body>`. Inline scripts at bottom of body run before `DOMContentLoaded` fires (the event fires after the parser reaches `</html>`, which is after all synchronous scripts). The `addEventListener('DOMContentLoaded', ...)` will register and fire correctly.
- **Status:** PASS

---

#### TC-22 — `postJson` and `getJson` helper functions defined
- **Pre-condition:** Read JS lines 291-306
- **Steps:** Verify both functions exist and include CSRF header
- **Expected:** Both functions present with `X-CSRFToken` header
- **Actual:** `postJson` (line 291) sends POST with `Content-Type: application/json` and `X-CSRFToken`. `getJson` (line 302) sends GET with `X-CSRFToken`. CORRECT.
- **Status:** PASS

---

#### TC-23 — CSRF handling in all AI fetch calls
- **Pre-condition:** Read JS lines 284-306, 310, 389, 409, 505
- **Steps:** Verify every fetch call that modifies state includes CSRF token
- **Expected:** All POST endpoints send CSRF token
- **Actual:** `postJson` includes `X-CSRFToken` on every call. `getJson` includes it too. The generate-insights GET fetch (line 394) also includes the header. All POST endpoints pass CSRF. CORRECT.
- **Status:** PASS

---

#### TC-24 — `btn-new-chat` resets `chatHistory` array and DOM
- **Pre-condition:** Read JS lines 553-564
- **Steps:** Verify new chat resets state
- **Expected:** `chatHistory = []`, DOM replaced with welcome message, chips shown
- **Actual:** Line 554: `chatHistory = []`. Line 555-562: `container.innerHTML` replaced. Line 563: `chat-chips` unhidden. CORRECT.
- **Status:** PASS

---

#### TC-25 — OpenAI SDK v2 compatibility in `AIService`
- **Pre-condition:** `openai==2.29.0` installed; read `insights/services.py` lines 102-108, 163-169
- **Steps:** Verify API method calls match SDK v2 interface
- **Expected:** `client.chat.completions.create(...)` with `response.choices[0].message.content`
- **Actual:** Both `_call_ai` and `_call_ai_messages` use this pattern. Compatible with openai v2.x.
- **Status:** PASS

---

#### TC-26 — `_render_markdown` `<ol>` greedy DOTALL wrapping
- **Pre-condition:** Run manual test with non-consecutive numbered list items
- **Steps:** Pass `'1. Item\n\nText\n\n2. Item'` through `_render_markdown`
- **Expected:** Clean `<ol>` wrapping only around list items
- **Actual:** The greedy `re.DOTALL` regex wraps from first `<li>` to last `</li>`, capturing intermediate non-list content inside the `<ol>`. Produces malformed HTML like `<ol><li>Item</li></p><p>Text</p><p><li>Item</li></ol>`. Browsers tolerate this but it is semantically broken.
- **Status:** FAIL
- **See:** BUG-03

---

#### TC-27 — Design system compliance: card colors
- **Pre-condition:** Read `templates/insights/index.html`; read `docs/design-system.md`
- **Steps:** Compare card background and border classes against spec
- **Expected:** Cards use `bg-zinc-900 border border-zinc-800`
- **Actual:** All 5 AI cards and the chat panel use `bg-zinc-900 border border-zinc-800`. CORRECT.
- **Status:** PASS

---

#### TC-28 — Design system compliance: button gradients
- **Pre-condition:** Read template button classes; read design system
- **Steps:** Verify primary CTA buttons
- **Expected:** Primary buttons use `from-green-500 to-emerald-600`
- **Actual:** `btn-suggest-next` and `btn-chat-send` use `from-green-500 to-emerald-600` (primary). Other buttons use thematic gradients (`sky`, `violet`, `emerald/teal`) that are contextually appropriate and not defined as violations in the spec. The design system only mandates green/emerald for the primary CTA; it does not prohibit secondary themed buttons.
- **Status:** WARN
- **Note:** The spec is silent on non-primary button gradient variants. `btn-generate-insights` uses `from-sky-500 to-blue-600` and `btn-analyze-topics` uses `from-violet-500 to-purple-600`. These are thematic but outside the strict spec pattern. Flag for design team review.

---

### Bugs Found

#### BUG-01 — Self-XSS: Forgotten content title inserted into innerHTML without escaping
- **Severity:** Medium
- **Component:** `templates/insights/index.html` (JavaScript, lines 335-340)
- **Description:** When building the forgotten content list HTML, `item.title` from the server JSON response is inserted directly into an innerHTML string via concatenation. No client-side HTML escaping is applied. A content title containing HTML metacharacters (e.g., `"><img src=x onerror=alert(1)>`) would break the HTML structure or execute injected code. Since content is user-scoped, this is self-XSS rather than cross-user XSS, but it still violates safe coding practice and represents an unintended attack surface (e.g., via a malicious URL that auto-sets a title).
- **Reproduction:**
  1. Create a content item with title: `"><img src=x onerror="alert(document.cookie)">`
  2. Do not start studying it for 30+ days (or manually set `created_at` to 31 days ago)
  3. Visit `/insights/`
  4. Observe forgotten content list renders with broken HTML; `onerror` attribute executes
- **Expected vs Actual:** Title should be HTML-escaped (e.g., using a helper like `escapeHtml`) before insertion into innerHTML. Currently no escaping is applied.
- **Suggested fix:** Define and use `escapeHtml(item.title)` in the forgotten content list builder, matching the `escapeHtml` function already defined in the same script block.

---

#### BUG-02 — `_render_markdown`: bullet list items not wrapped in `<ul>`
- **Severity:** Low
- **Component:** `insights/views.py` — `_render_markdown()` function (lines 25-26)
- **Description:** The `_render_markdown` function converts bullet list syntax (`- item` and `• item`) to `<li>` tags but never wraps them in a `<ul>` parent element. Numbered list items ARE wrapped in `<ol>` (line 23), but the equivalent step for bullet lists is absent. The output is `<p><li>...</li><br><li>...</li></p>` which is invalid HTML5 (`<li>` cannot be a direct child of `<p>`). While modern browsers render this reasonably, it may cause layout issues with `prose` Tailwind classes applied to the result container.
- **Reproduction:**
  1. Call any AI endpoint that returns bullet-formatted output (e.g., `generate-insights`, which prompts for "3-5 bullet points")
  2. Inspect the rendered HTML in the `#insights-result` div
  3. Observe `<li>` elements directly inside `<p>`, with no surrounding `<ul>`
- **Expected vs Actual:** Expected `<ul class="list-disc list-inside space-y-1"><li>...</li></ul>`. Actual: bare `<li>` elements inside `<p>`.
- **Suggested fix:** After the bullet `re.sub` at line 25, add a wrapping step analogous to line 23: `re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul class="list-disc list-inside space-y-1">\1</ul>', text, flags=re.DOTALL)`.

---

#### BUG-03 — `_render_markdown`: greedy `<ol>` regex absorbs non-list content between list items
- **Severity:** Low
- **Component:** `insights/views.py` — `_render_markdown()` function (line 23)
- **Description:** The `<ol>` wrapping regex `re.sub(r'(<li>.*</li>)', ...)` uses `re.DOTALL` and is greedy, causing it to match from the very first `<li>` in the string to the very last `</li>`. Any non-list text that appears between numbered list items (separated by blank lines in the AI response) gets captured inside the `<ol>`. The resulting HTML is structurally invalid. Browsers may recover, but the visual output may deviate from intent.
- **Reproduction:**
  1. Trigger an AI response that includes a numbered list with a paragraph of text in between items (e.g., `1. Item\n\nExplanation paragraph\n\n2. Item`)
  2. Pass this string through `_render_markdown`
  3. Inspect output: the paragraph is inside the `<ol>`
- **Expected vs Actual:** Expected: paragraph rendered outside the `<ol>`. Actual: paragraph inside `<ol>`, producing `<ol><li>Item</li></p><p>Explanation</p><p><li>Item</li></ol>` (invalid).
- **Suggested fix:** Use a non-greedy match or restructure the approach to collect only consecutive `<li>` blocks before wrapping.

---

### Passing Checks Summary

| Area | Result |
|---|---|
| Django system check | PASS — 0 issues |
| All 5 new views present with `LoginRequiredMixin` | PASS |
| All 5 new URL patterns registered | PASS |
| `build_user_context` module-level, lazy model imports | PASS |
| `AIService` has all 5 new methods | PASS |
| `DashboardService.get_forgotten_contents` query correctness | PASS |
| `ForgottenContentsView` JSON response structure | PASS |
| `ChatView` history deduplication | PASS |
| `_render_markdown` HTML escaping (XSS from AI output) | PASS |
| Chat assistant message XSS safety | PASS |
| Two-column `lg:grid-cols-12` layout | PASS |
| All required element IDs present | PASS |
| Starter chips with `data-chip` attributes | PASS |
| `DOMContentLoaded` timing for auto-load | PASS |
| `postJson`/`getJson` with CSRF headers | PASS |
| `generate-insights` GET endpoint still functional | PASS |
| `generate-insights` JS `insights`-to-`html` transform | PASS |
| New chat button resets `chatHistory` and DOM | PASS |
| OpenAI SDK v2 API compatibility | PASS |
| Design system: card backgrounds/borders | PASS |

---

### Notes

1. **Zero test coverage for Sprint 8:** All `tests.py` files remain empty stubs. The Sprint 8 features (`SuggestNextView`, `ForgottenContentsView`, `AnalyzeTopicsView`, `WeeklySummaryView`, `ChatView`, `DashboardService.get_forgotten_contents`, `AIService.chat`) have no automated test coverage. This is a recurring pattern across all sprints in this project.

2. **Model name validity:** `AIService.ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001'` — the model ID format is non-standard (typically `claude-haiku-3-5-20241022`). The version suffix `4-5` and date `20251001` are unusual. This cannot be verified statically and may result in API errors at runtime. Recommend verifying against the Anthropic API model catalog.

3. **`generate-insights` response format mismatch handled correctly:** The existing `GenerateInsightsView` returns `{success, insights}` while all new views return `{success, html}`. The JS correctly handles both via the inline transform on lines 399-401. No regression.
