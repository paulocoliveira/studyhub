# Agents

AI agents specialized in the StudyHub stack. Each agent covers a specific discipline in the development workflow.

## Index

| Agent | File | When to use |
|---|---|---|
| [Backend Developer](#backend-developer) | `backend.md` | Models, views, forms, URLs, migrations, admin, AI integration |
| [Frontend Developer](#frontend-developer) | `frontend.md` | HTML templates, DTL, TailwindCSS, JavaScript |
| [QA / Tester](#qa--tester) | `qa.md` | End-to-end testing, UI verification, bug reports |

---

## Backend Developer

**File:** `backend.md`
**MCP:** context7 (Django docs)

Implements everything that runs on the server: models, class-based views, forms, URL routing, migrations, Django admin, and business logic. Also owns the AI integration in the `insights` app via the Anthropic SDK.

**Use when:**
- Creating or changing a Django model and its migration
- Implementing a new view, form, or URL route
- Adding filtering, search, or sorting to a queryset
- Working on authentication (custom user model, login, registration)
- Implementing file upload handling or Open Graph URL fetching
- Integrating or updating the Claude AI features

---

## Frontend Developer

**File:** `frontend.md`
**MCP:** context7 (TailwindCSS docs)

Builds all HTML templates using Django Template Language and styles them with TailwindCSS following the project design system defined in `docs/design-system.md`. Handles responsiveness, accessibility, and vanilla JS behaviour.

**Use when:**
- Creating a new page or template
- Updating the layout, components, or styles of an existing page
- Implementing the card/list view toggle with `localStorage` persistence
- Building form templates with inline validation error rendering
- Working on the sidebar, navigation, or base templates
- Ensuring responsive behaviour across mobile, tablet, and desktop

---

## QA / Tester

**File:** `qa.md`
**MCP:** Playwright (browser automation)

Performs end-to-end tests against the running development server. Verifies functional correctness, design system compliance, responsiveness, and edge cases. Produces structured test reports and bug reports saved to `aireports/`.

**Use when:**
- A sprint or feature is complete and ready for testing
- Verifying that a bug fix actually resolves the issue
- Checking UI compliance against the design system
- Testing responsive layouts at mobile, tablet, and desktop breakpoints
- Running regression tests after a significant change

---

## MCP Server Requirements

| MCP Server | Used by | Purpose |
|---|---|---|
| `context7` | Backend, Frontend | Fetch up-to-date library docs (Django, TailwindCSS) |
| `playwright` | QA | Browser automation for end-to-end testing |
