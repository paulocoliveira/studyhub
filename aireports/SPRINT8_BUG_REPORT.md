# Sprint 8 — Bug Report
## StudyHub — Advanced AI & Learning Intelligence

**Date:** 2026-03-26
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA static analysis (source code review + logic tracing)
**Total bugs:** 3
**Fixed:** 3 (all fixed immediately during QA)

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Medium | `templates/insights/index.html` | Fixed |
| [B-02](#b-02) | Low | `insights/views.py` — `_render_markdown` | Fixed |
| [B-03](#b-03) | Low | `insights/views.py` — `_render_markdown` | Fixed |

---

## B-01

**Title:** Self-XSS via unescaped `item.title` in Forgotten Content list

**Severity:** Medium
**Component:** `templates/insights/index.html`
**Status:** Fixed
**Discovered in:** QA static analysis — JS innerHTML construction
**Fix date:** 2026-03-26

### Description

The Forgotten Content list is rendered client-side by constructing an HTML string and assigning it to `list.innerHTML`. The content title (`item.title`) was concatenated directly into the string without HTML escaping. A title containing `"><img src=x onerror=alert(1)>` would execute arbitrary JavaScript in the user's own session.

### Steps to reproduce

1. Log in as a user
2. Create a content item with title: `"><img src=x onerror=alert(1)>`
3. Set `created_at` to 31+ days ago manually (via shell or admin)
4. Navigate to `/insights/`
5. Observe the Forgotten Content section — the injected script executes

### Expected behavior

Content titles must be HTML-escaped before insertion into innerHTML.

### Actual behavior

```javascript
// Before fix
html += '...<a ...>' + item.title + '</a>...'  // unescaped
```

### Root cause

The `escapeHtml(text)` helper was defined in the same script block but was not applied to `item.title` in the forgotten content list builder.

### Fix applied

**File:** `templates/insights/index.html`

```javascript
// After fix
var safeTitle = escapeHtml(item.title);
html += '...<a ... title="' + safeTitle + '">' + safeTitle + '</a>...'
```

### Impact

Self-XSS only (attacker must control their own data). However, it violates secure coding principles and could be escalated in shared/multi-tenant environments or via CSRF-forced content creation.

---

## B-02

**Title:** Bullet list items rendered as bare `<li>` outside `<ul>` wrapper

**Severity:** Low
**Component:** `insights/views.py` — `_render_markdown()`
**Status:** Fixed
**Discovered in:** QA static analysis — regex output tracing
**Fix date:** 2026-03-26

### Description

`_render_markdown()` converts `- item` and `• item` lines to `<li>` elements (correct) but did not wrap consecutive bullet items in a `<ul>` container. This produced invalid HTML5: bare `<li>` elements inside a `<p>` tag. All AI responses that use bullet points (notably `generate_insights` which explicitly prompts for bullet points) were affected.

### Expected behavior

```html
<ul class="list-disc list-inside space-y-1">
  <li>Bullet A</li>
  <li>Bullet B</li>
</ul>
```

### Actual behavior (before fix)

```html
<p><li>Bullet A</li><br><li>Bullet B</li></p>
```

### Root cause

The bullet list regex converted markers to `<li>` tags but the subsequent `<ul>` wrapping step was missing. The numbered list section had a `<ol>` wrap step; the bullet section did not.

### Fix applied

**File:** `insights/views.py`

Added a two-step approach using a placeholder tag `<blt>` to avoid collision with existing `<li>` from numbered lists, then wrapping groups of `<blt>` tags in `<ul>`:

```python
text = re.sub(r'(?m)^[-•] (.+)$', r'<blt>\1</blt>', text)
text = re.sub(
    r'((?:<blt>[^<]*</blt>\n?)+)',
    lambda m: '<ul class="list-disc list-inside space-y-1">'
        + m.group(1).replace('<blt>', '<li>').replace('</blt>', '</li>')
        + '</ul>',
    text,
)
text = re.sub(r'<blt>(.*?)</blt>', r'<li>\1</li>', text)  # cleanup any stragglers
```

### Impact

Visual — bullet-point AI responses rendered without proper list structure, making them harder to read.

---

## B-03

**Title:** Greedy `re.DOTALL` regex wraps non-list content inside `<ol>` tags

**Severity:** Low
**Component:** `insights/views.py` — `_render_markdown()`
**Status:** Fixed
**Discovered in:** QA static analysis — regex flag analysis
**Fix date:** 2026-03-26

### Description

The regex for wrapping numbered list items in `<ol>` used `re.sub(r'(<li>.*</li>)', ..., flags=re.DOTALL)`. With `re.DOTALL`, the `.` matches newlines, making `.*` greedy across the entire string. Any text between the first `<li>` and the last `</li>` — including paragraph text and other HTML — was incorrectly captured inside the `<ol>`, producing structurally invalid HTML.

### Example

Input AI response:
```
1. First item

Some paragraph text.

2. Second item
```

Expected output: two separate `<ol>` elements with the paragraph between them.

Actual output (before fix): one `<ol>` containing both items AND the paragraph text inside.

### Root cause

The `re.DOTALL` flag was passed to the substitution, combined with a greedy `.*` quantifier, causing over-capture. The correct approach is to match only sequences of consecutive `<li>` lines.

### Fix applied

**File:** `insights/views.py`

Replaced the greedy pattern with a non-DOTALL pattern that matches consecutive `<li>` lines only:

```python
# Before (buggy)
text = re.sub(r'(<li>.*</li>)', r'<ol ...>\1</ol>', text, flags=re.DOTALL)

# After (fixed)
text = re.sub(r'((?:<li>[^<]*</li>\n?)+)', r'<ol class="list-decimal list-inside space-y-1">\1</ol>', text)
```

`[^<]*` prevents crossing tag boundaries, and removing `re.DOTALL` ensures the pattern matches within a line.

### Impact

AI responses with numbered lists followed by paragraph text would render with the paragraph incorrectly inside the list container, breaking the visual hierarchy.

---

## Fix Summary

| ID | File modified | Change | Tests broken |
|----|--------------|--------|--------------|
| B-01 | `templates/insights/index.html` | Wrap `item.title` in `escapeHtml()` | None |
| B-02 | `insights/views.py` | Add `<ul>` wrapper for bullet list items | None |
| B-03 | `insights/views.py` | Replace greedy `re.DOTALL` regex with non-greedy line-bounded pattern | None |
