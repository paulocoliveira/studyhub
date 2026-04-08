# StudyHub — Hackathon Testing Guidelines
### The Test Tribe Porto · Meetup Hackathon

---

## Welcome

You're about to test **StudyHub**, a real web application built in Python and Django.

Your team's mission is to explore, understand, and test this system — identifying issues, risks, and improvement opportunities that a real QA team would care about.

Improvements are also very welcome.

This document describes the system as it **should work**. Use it as the source of truth for expected behaviour when designing your test strategy.

---

## Hackathon Setup & Instructions

### 1. Bug Tracking Tool (Start Here)

Before doing anything else:

👉 Access the bug tracking tool:  
https://gira.paulocoliveira.com/

- Create your account
- After creating your account, **associate yourself with a project that has your team's name**

⚠️ This is the **first step** and must be completed before starting testing.

All bugs, issues, and observations should be logged there.

---

### 2. Application Under Test

👉 StudyHub application:  
https://studyhub.paulocoliveira.com/

This is the system your team will test during the hackathon.

---

### 3. OpenAI API Keys (Per Team)

Each team will receive an OpenAI API key to use AI features inside the application.

> ⚠️ Use only your team's key. Do not share across teams.

| Team | API Key |
|------|--------|
| Team 1 | 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 |
| Team 2 | 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 |
| Team 3 | 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 |
| Team 4 | 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 |
| Team 5 | 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 |
| Team 6 | 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 |
| Team 7 | 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 |
| Team 8 | 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 |
| Team 9 | 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 |
| Team 10 | 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 |

These keys are required to test AI-powered features.

---

### 4. Testing Guidelines

Your team is free to explore the system in your own way. 

---

### 5. Important Restrictions

🚫 Do **NOT** perform:

- Performance testing (load, stress, spike)
- Any tests intended to overload, break, or degrade the hosting server

Focus on realistic QA scenarios.

---

### 6. Final Presentation (3 minutes)

At the end of the session, your team will present your work.

Focus on:

- The **team’s experience during the hackathon**
- The **strategy you chose and why**
- The **approach and techniques used**
- The **key learnings and insights from your testing**

> ⚠️ Avoid turning this into a bug list presentation — focus on how you worked and what you learned. You don't need a ppt, we prefer speaking only.

---

## What is StudyHub?

StudyHub is a **personal learning content management system**. It helps self-learners, students, and professionals centralize and organize their learning materials — articles, videos, courses, podcasts, books, PDFs — scattered across multiple platforms, into one organized workspace.

### Core idea
A user saves content (by URL or file upload), categorizes it, tracks their progress through it (New → In Progress → Completed), and uses AI features to get help with categorization, descriptions, and study insights.

### Who uses it?
- Self-learners who save content from YouTube, newsletters, podcasts, blogs
- Professionals curating knowledge in their field (QA, AI, dev, design)
- Students organizing study materials
- Anyone with a chaotic bookmarks folder

---

## Application Pages & Features

### Public Area (unauthenticated)

#### Landing Page
- Presents the product with a value proposition, features, and benefits
- Two CTAs: **Sign Up** and **Log In**
- Accessible without authentication

#### Registration (`/users/register/`)
- Fields: **Full name**, **Email**, **Password**, **Confirm password**
- Email must be unique per user
- After registration, user is redirected to login

#### Login (`/users/login/`)
- Credential is **email** (not username)
- After successful login, redirect to Dashboard

---

### Authenticated Area

All pages below require the user to be logged in. Unauthenticated access redirects to the login page.

---

### Dashboard (`/dashboard/`)

The main hub. Shows an aggregated overview of the user's library.

**Sections:**
- **Onboarding panel** — shown only when the library is empty, with shortcuts to add content, create a category, or create a tag
- **Summary statistics** — total items, count by status (New / In Progress / Completed)
- **Content by Type** — breakdown of items per content type (Article, Video, Podcast, etc.), each linking to the filtered content list
- **Recently Added** — the last items saved, with links to their detail pages
- **Recently Completed** — items most recently marked as Completed
- **Top Categories** — categories with the highest number of items
- **Top Tags** — tags with the highest number of items

---

### Content List (`/contents/`)

The main content library. Shows all of the user's saved items.

**Features:**
- **Search** — full-text search across title and description
- **Filter by Status** — New / In Progress / Completed
- **Filter by Type** — Article, Video, Podcast, Course, Book, Tool, Other
- **Filter by Category** — dropdown of the user's categories
- **Sort** — Newest first, Oldest first, Title A–Z, Title Z–A, Category
- **Hide Completed toggle** — active by default; hides completed items from the list. Can be toggled to show them. State is preserved across filter submissions
- **View toggle** — switch between **Card Grid** and **List** view. Preference persists in `localStorage` across page reloads
- **Pagination** — 12 items per page
- **Clear all filters** — visible only when actual filters (search, status, type, category) are active

**Card view** — each card shows:
- Thumbnail image (Open Graph preview from URL, or a placeholder icon per content type)
- Content type badge (top left overlay)
- Status badge (top right overlay)
- Title (clickable — goes to detail)
- Image/placeholder area (clickable — goes to detail)
- Description snippet
- Category
- Tags (up to 3 visible + overflow count)
- Date added
- View / Edit actions

**List view** — each row shows:
- Content type badge
- Status badge
- Title (clickable — goes to detail)
- Category
- Date added
- Tags (up to 3)
- View / Edit / Delete actions

---

### Add / Edit Content (`/contents/create/`, `/contents/<id>/edit/`)

A form to create or update a content entry.

**Fields:**

| Field | Required | Notes |
|---|---|---|
| URL | No | Paste a link; metadata (title, description, preview image) is auto-fetched on blur |
| Title | Yes | Auto-populated from URL metadata if empty |
| Type | Yes | Article, Video, Podcast, Social Media Post, Social Media Profile, PDF, Course, Other |
| Status | No | New (default), In Progress, Completed |
| Category | No | Dropdown of user's categories. **Auto-suggested by AI** silently after URL metadata fetch or title blur (only if no category is selected yet). User can change it |
| Description | No | Free text. Can be AI-generated via the "✨ AI Generate" button |
| Tags | No | Checkbox multi-select of the user's tags |
| File | No | Upload a local file as an alternative to a URL |

**Behaviour:**
- When a URL is pasted and the field loses focus: the system fetches Open Graph metadata and auto-fills title and description (if empty), auto-detects content type from URL patterns (e.g. YouTube → Video, Spotify → Podcast)
- After title is populated, category is silently suggested by AI from the user's existing category list (no button needed)
- An "✨ AI suggested" label appears next to Category when AI made a suggestion; disappears when the user manually changes it
- File upload validates extension and size (max 10 MB) client-side and server-side
- Form validates required fields (title, type) before submit

**Allowed file types:** PDF, JPG, JPEG, PNG, GIF, WebP, MP3, MP4, DOC, DOCX, TXT, MD

---

### Content Detail (`/contents/<id>/`)

Shows all information for a single content item.

**Sections:**
- Title with content type and status badges
- URL (clickable external link)
- File download link (if a file was uploaded)
- Category
- Tags
- Description
- Created / Last updated dates

**Actions:**
- **Edit** — navigates to the edit form
- **Delete** — navigates to confirmation page
- **Quick status change** — buttons to move the item to any status not currently active (e.g. "Mark as Completed")

**Navigation:**
- Back to Contents link and breadcrumb restore the previous filter/sort state (filters applied before entering the detail page are preserved on return)

---

### Categories (`/categories/`)

Manage the user's personal categories.

**Rules:**
- Categories are **user-scoped** — each user has their own, isolated set
- Each category has a **name** (required) and an optional **description**
- Category names must be **unique per user**
- Deleting a category **does not delete its contents** — items in that category have their category set to null
- The list shows each category with its **item count**

**Actions:** Create, Edit, Delete

---

### Tags (`/tags/`)

Manage the user's personal tags.

**Rules:**
- Tags are **user-scoped**
- Each tag has a **name** (required)
- Tags have a many-to-many relationship with content items
- Deleting a tag removes it from all associated content
- The list shows each tag with its **item count**

**Actions:** Create, Delete (no edit)

---

### AI Insights (`/insights/`)

A dedicated page with AI-powered features about the user's learning library.

> All AI features are **user-triggered** (never automatic). The system must work fully if the AI service is unavailable.

**Features:**

#### Consumption Insights
Analyzes total items, status distribution, and content type breakdown. Returns 3–5 bullet points of insights and 2–3 actionable suggestions.

#### What to Study Next
Analyzes items marked as New or In Progress. Recommends 3–5 items to study next, with a one-line reason for each. Based on recency, category patterns, and consumption history.

#### Forgotten Content
Surfaces items saved more than 30 days ago that are still in **New** status — never progressed. The user can click each to review, study, or delete.

#### Topic Patterns
Analyzes the user's top categories and tags. Identifies recurring study themes and suggests 2–3 directions for deeper exploration.

#### Weekly Summary
Generates a concise 2–3 sentence narrative covering: items completed this week, items added, items in progress, and the most active category or tag.

#### AI Chat — Learning Assistant
A multi-turn chat interface where the user can ask natural language questions about their own library data.

**How it works (RAG-style):**
Before each AI call, the system builds a full structured snapshot of the user's library from the database — all content titles, types, statuses, categories, tags, and descriptions — and injects it as context into the AI prompt alongside the user's question.

**Strict grounding rules:**
- The assistant answers **only** based on the user's saved data
- If something is not in the library, it says "I don't see that in your library"
- It never recommends content, books, or resources outside the user's saved list
- It never searches the internet or uses external knowledge
- It may reason about patterns and counts within the data

**Chat behaviour:**
- Supports multi-turn conversation within the session
- History is kept in the browser only — resets on page reload, never persisted to the database
- Daily limit of 20 messages
- Errors are displayed inline without crashing the page

---

### User Settings

#### Change Password (`/users/password-change/`)
- Requires current password
- New password must be confirmed
- On success, redirected to Dashboard

#### Logout
- Available from the navigation on all authenticated pages
- Clears the session and redirects to the landing page

---

## Data Model Summary

```
USER
  id, email (unique), first_name, last_name, password
  created_at, updated_at

CATEGORY (user-scoped)
  id, name, description, user_id
  created_at, updated_at
  Constraint: unique(name, user)

TAG (user-scoped)
  id, name, user_id
  created_at, updated_at

CONTENT (user-scoped)
  id, title, url (optional), content_type, description (optional)
  status, preview_image_url (optional), file (optional)
  user_id, category_id (nullable, SET NULL on category delete)
  created_at, updated_at

CONTENT ↔ TAG  (many-to-many)
```

**Content types:** `article`, `video`, `podcast`, `social_media_post`, `social_media_profile`, `pdf`, `course`, `other`

**Status values:** `new`, `in_progress`, `completed`

---

## Non-Functional Requirements

| # | Area | Expected behaviour |
|---|---|---|
| NFR-01 | Responsive design | Fully functional on desktop (1024px+), tablet (768px), and mobile (375px) |
| NFR-02 | Dark theme | Consistent dark UI with gradient accents throughout |
| NFR-03 | Performance | Pages should load within 2 seconds |
| NFR-04 | Security | CSRF protection on all forms, login required for all authenticated views, data is user-scoped (no user sees another user's data) |
| NFR-05 | Accessibility | Semantic HTML, proper labels, keyboard navigation |
| NFR-06 | Browser support | Chrome, Firefox, Safari, Edge — latest 2 versions |
| NFR-07 | Error handling | AI errors show inline messages without crashing the page. Form errors shown inline per field |
| NFR-08 | Data isolation | Users can only see and operate on their own data |

---

*Good luck!*