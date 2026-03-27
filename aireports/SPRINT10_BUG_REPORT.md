# Sprint 10 — Bug Injection Ledger
## StudyHub — QA Hackathon

**Date:** 2026-03-26
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Purpose:** Intentional bug injection for The Test Tribe Porto hackathon — participants must find and document these defects
**Total bugs injected:** 20
**Verification status:** 18 confirmed via automated tests · 2 require browser testing (JS/template bugs)

> **ORGANISER EYES ONLY — do not share this file with hackathon participants.**

---

## Index

| ID | Severity | Domain | Component | Test coverage |
|----|----------|--------|-----------|---------------|
| [B-01](#b-01) | Medium | Auth | `core/settings.py` | Automated ✅ |
| [B-02](#b-02) | High | Auth | `users/forms.py` | Automated ✅ |
| [B-03](#b-03) | High | Auth | `users/views.py` | Automated ✅ |
| [B-04](#b-04) | Medium | Content | `contents/forms.py`, `contents/models.py` | Automated ✅ |
| [B-05](#b-05) | High | Content | `contents/views.py` | Automated ✅ |
| [B-06](#b-06) | Critical | Content | `contents/views.py` | Automated ✅ |
| [B-07](#b-07) | Low | Content | `contents/views.py` | Automated ✅ |
| [B-08](#b-08) | High | Content | `contents/views.py` | Automated ✅ |
| [B-09](#b-09) | Low | Content | `contents/views.py` | Automated ✅ |
| [B-10](#b-10) | Critical | Categories | `contents/models.py` | Automated ✅ |
| [B-11](#b-11) | High | Categories | `categories/models.py` | Automated ✅ |
| [B-12](#b-12) | Low | Tags | `tags/views.py` | Automated ✅ |
| [B-13](#b-13) | Medium | Tags | `tags/views.py` | Automated ✅ |
| [B-14](#b-14) | Medium | Dashboard | `dashboard/services.py` | Automated ✅ |
| [B-15](#b-15) | High | Dashboard | `dashboard/services.py` | Automated ✅ |
| [B-16](#b-16) | Medium | AI / UI | `templates/contents/content_form.html` | Browser 🌐 |
| [B-17](#b-17) | Low | UI | `contents/views.py` | Automated ✅ |
| [B-18](#b-18) | Medium | UI | `templates/components/sidebar.html` | Browser 🌐 |
| [B-19](#b-19) | High | AI | `insights/views.py` | Automated ✅ |
| [B-20](#b-20) | High | AI / Security | `insights/services.py`, template | Browser 🌐 |

---

## B-01

**Title:** Registration accepts passwords shorter than 8 characters

**Severity:** Medium
**Domain:** Authentication
**Component:** `core/settings.py`
**Status:** Injected — Active

### Description
Users can register with extremely short passwords (e.g., "ab", "1") without receiving any validation error. The `MinimumLengthValidator` was removed from `AUTH_PASSWORD_VALIDATORS`.

### Steps to reproduce
1. Navigate to `/users/register/`
2. Fill in name, email, password: "ab", confirm password: "ab"
3. Submit the form
4. Observe: registration succeeds, user is redirected to login

### Expected behavior
Form error: "This password is too short. It must contain at least 8 characters."

### Actual behavior
Registration succeeds with a 2-character password.

### Code change
```python
# core/settings.py — MinimumLengthValidator entry removed from AUTH_PASSWORD_VALIDATORS
```

---

## B-02

**Title:** Login error message reveals whether the email address exists in the system

**Severity:** High
**Domain:** Authentication
**Component:** `users/forms.py` — `EmailAuthenticationForm`

### Description
The login form emits distinct error messages depending on whether the email exists. This is an account enumeration vulnerability — an attacker can probe which email addresses are registered.

### Steps to reproduce
1. Navigate to `/users/login/`
2. Enter an email that IS registered + wrong password → error: **"Password is incorrect. Please try again."**
3. Enter an email that is NOT registered + any password → error: **"No account found with this email address."**
4. Compare the two messages — they reveal whether the email exists

### Expected behavior
Single generic message in both cases: "Please enter a correct email and password."

### Actual behavior
Two distinct messages leak account existence.

### Code change
```python
# users/forms.py — clean() overridden to emit different messages based on User.objects.filter(email=...).exists()
```

---

## B-03

**Title:** After changing password, user session is invalidated and user is logged out

**Severity:** High
**Domain:** Authentication
**Component:** `users/views.py` — `CustomPasswordChangeView`

### Description
After a successful password change, the user's session token becomes invalid. The success message is displayed, but the very next authenticated request redirects to the login page. The user effectively logs themselves out every time they change their password.

### Steps to reproduce
1. Log in with any account
2. Navigate to `/users/password-change/`
3. Fill in current password and a new valid password; submit
4. Observe "Password changed successfully" message
5. Navigate to `/dashboard/` or any authenticated page
6. Observe redirect to `/users/login/` — session was invalidated

### Expected behavior
User remains logged in with the new password; session is preserved via `update_session_auth_hash`.

### Actual behavior
Session is invalidated. User is redirected to login on the next request.

### Code change
```python
# users/views.py — form_valid calls form.save() and redirects manually without update_session_auth_hash()
```

---

## B-04

**Title:** Creating content without a title silently saves an empty-titled item

**Severity:** Medium
**Domain:** Content
**Component:** `contents/forms.py`, `contents/models.py`

### Description
The title field is no longer required. Submitting the content creation form with an empty title saves a content item with `title=""`. The content list shows a blank card with no title.

### Steps to reproduce
1. Navigate to `/contents/create/`
2. Leave the title field empty; fill in only content type
3. Submit the form
4. Observe: redirect to list, a new card with no title is visible

### Expected behavior
Form error: "This field is required."

### Actual behavior
Content saves with empty title (HTTP 302 redirect).

### Code change
```python
# contents/forms.py — title field set to required=False
# contents/models.py — title field has blank=True; migration 0003 applied
```

---

## B-05

**Title:** Status filter results are inverted — selecting "Completed" shows everything except completed

**Severity:** High
**Domain:** Content
**Component:** `contents/views.py` — `ContentListView`

### Description
The status filter uses `.exclude()` instead of `.filter()`. Selecting "Completed" returns all non-completed items; selecting "New" returns all non-new items.

### Steps to reproduce
1. Create several items with different statuses (New, In Progress, Completed)
2. Navigate to `/contents/` and apply the "Completed" filter
3. Observe: In Progress and New items are shown; Completed items are hidden

### Expected behavior
Only Completed items should be shown.

### Actual behavior
All items EXCEPT Completed are shown.

### Code change
```python
# contents/views.py — qs.filter(status=status) changed to qs.exclude(status=status)
```

---

## B-06

**Title:** Any authenticated user can edit another user's content via direct URL manipulation

**Severity:** Critical
**Domain:** Content
**Component:** `contents/views.py` — `ContentUpdateView`

### Description
`ContentUpdateView.get_queryset` returns all content objects without filtering by the current user. Any authenticated user who knows (or guesses) a content ID can navigate to `/contents/<id>/edit/` and edit another user's content.

### Steps to reproduce
1. Log in as User A, note the edit URL for one of User A's items (e.g., `/contents/5/edit/`)
2. Log out; log in as User B
3. Navigate directly to `/contents/5/edit/`
4. Observe: User A's content form is displayed and editable

### Expected behavior
HTTP 404 — User B cannot access User A's content.

### Actual behavior
HTTP 200 — User B can view and submit the edit form for User A's content.

### Code change
```python
# contents/views.py — get_queryset returns Content.objects.all() instead of filtering by user
```

---

## B-07

**Title:** "Oldest first" sort produces the same result as "Newest first"

**Severity:** Low
**Domain:** Content
**Component:** `contents/views.py` — `ContentListView`

### Description
When the user selects "Oldest first" (sort=`created_at`), the view applies `-created_at` (descending) instead of `created_at` (ascending). Both sort options produce identical results — newest first.

### Steps to reproduce
1. Create several content items at different times
2. Sort by "Newest first" → note the order
3. Sort by "Oldest first" → observe the same order

### Expected behavior
"Oldest first" should show the earliest-added item at the top.

### Actual behavior
Both options show the most recently added item at the top.

### Code change
```python
# contents/views.py — sort == 'created_at' branch applies order_by('-created_at') instead of 'created_at'
```

---

## B-08

**Title:** "Mark as Completed" sets status to "In Progress" instead

**Severity:** High
**Domain:** Content
**Component:** `contents/views.py` — `ContentStatusUpdateView`

### Description
When a user clicks "Mark as Completed", the status is silently saved as `in_progress`. The badge on the item changes to "In Progress" despite the user's intent to complete it. Items can never be marked as Completed through this UI.

### Steps to reproduce
1. Open any content item in the detail view
2. Click "Mark as Completed"
3. Observe: the status badge changes to "In Progress" instead of "Completed"

### Expected behavior
Status should change to "Completed" and the badge should show "Completed".

### Actual behavior
Status is set to "In Progress".

### Code change
```python
# contents/views.py — ContentStatusUpdateView maps 'completed' → 'in_progress' before saving
```

---

## B-09

**Title:** Content list header always shows the total unfiltered item count

**Severity:** Low
**Domain:** Content
**Component:** `contents/views.py`, `templates/contents/content_list.html`

### Description
The item count badge in the header always shows the total number of items for the user, even when filters reduce the visible items to a smaller number. A user with 47 items who filters to 3 results still sees "47 items" in the header.

### Steps to reproduce
1. Add 10+ content items
2. Apply a status filter that matches only 1–2 items
3. Observe the count badge at the top of the page

### Expected behavior
The count should reflect the number of filtered results.

### Actual behavior
The count always shows the user's total unfiltered item count.

### Code change
```python
# contents/views.py — total_count context uses Content.objects.filter(user=user).count() (unfiltered)
# templates/contents/content_list.html — badge reads {{ total_count }} instead of {{ paginator.count }}
```

---

## B-10

**Title:** Deleting a category silently deletes all content items in that category

**Severity:** Critical
**Domain:** Categories
**Component:** `contents/models.py` — `Content.category` FK

### Description
The `category` foreign key on `Content` was changed from `on_delete=SET_NULL` to `on_delete=CASCADE`. When a user deletes a category, every content item associated with that category is permanently and silently deleted alongside it — with no warning.

### Steps to reproduce
1. Create a category "Python"
2. Add 5 content items to the "Python" category
3. Navigate to the category list and delete "Python"
4. Navigate to the content list
5. Observe: all 5 items that were in "Python" are gone

### Expected behavior
The category is deleted; its former content items remain with `category=null`.

### Actual behavior
All content in the category is deleted without warning.

### Code change
```python
# contents/models.py — category FK on_delete changed from SET_NULL to CASCADE; migration 0003 applied
```

---

## B-11

**Title:** Duplicate category names are allowed for the same user

**Severity:** High
**Domain:** Categories
**Component:** `categories/models.py`

### Description
The `unique_together = ['name', 'user']` constraint was removed from `Category.Meta`. Users can create multiple categories with identical names. This causes confusion in the category dropdown on the content form, and in the filter bar where the same name appears multiple times.

### Steps to reproduce
1. Create a category named "AI"
2. Create another category also named "AI"
3. Observe: both are saved without error; the category list shows two "AI" entries

### Expected behavior
Form error: "A category with this name already exists."

### Actual behavior
Both categories save successfully; duplicates accumulate.

### Code change
```python
# categories/models.py — unique_together removed from Meta; migration 0002 applied
```

---

## B-12

**Title:** Tag list always shows 0 contents for every tag

**Severity:** Low
**Domain:** Tags
**Component:** `tags/views.py` — `TagListView`

### Description
The queryset annotation that counts associated content items was replaced with a constant `Value(0)`. Every tag on the tag list page shows "0 contents" regardless of how many content items actually use it.

### Steps to reproduce
1. Create a tag and assign it to 5 content items
2. Navigate to `/tags/`
3. Observe: the tag shows "0 contents"

### Expected behavior
The tag should show the correct count of associated content items.

### Actual behavior
All tags show "0 contents".

### Code change
```python
# tags/views.py — annotation changed from Count('contents') to Value(0, output_field=IntegerField())
```

---

## B-13

**Title:** Deleting a tag shows "deleted successfully" but the tag is never removed

**Severity:** Medium
**Domain:** Tags
**Component:** `tags/views.py` — `TagDeleteView`

### Description
`TagDeleteView.form_valid` was overridden to redirect without calling `super().form_valid()`. The delete operation is never performed. The user sees the "Tag deleted successfully" success message and is redirected to the tag list — where the tag still appears, unchanged.

### Steps to reproduce
1. Create a tag "python"
2. Navigate to the tag delete confirmation page
3. Confirm the deletion
4. Observe "Tag deleted successfully" message
5. The tag "python" is still visible in the tag list

### Expected behavior
Tag is permanently deleted and no longer appears in the list.

### Actual behavior
Tag persists; "deleted" message is misleading.

### Code change
```python
# tags/views.py — form_valid redirects without deleting the tag object
```

---

## B-14

**Title:** "Recently Completed" dashboard section shows recently added items instead

**Severity:** Medium
**Domain:** Dashboard
**Component:** `dashboard/services.py`

### Description
The `get_recent_completed` method no longer filters by `status='completed'` and uses `order_by('-created_at')`. The "Recently Completed" section on the dashboard is now identical to the "Recently Added" section — both show the most recently created items regardless of their status.

### Steps to reproduce
1. Add several content items but do NOT mark any as completed
2. Navigate to `/dashboard/`
3. Observe: the "Recently Completed" section shows the same items as "Recently Added"

### Expected behavior
"Recently Completed" should only show items with `status='completed'`, ordered by `updated_at` descending.

### Actual behavior
Shows the most recently *created* items regardless of status.

### Code change
```python
# dashboard/services.py — filter(status='completed') removed; order changed to -created_at
```

---

## B-15

**Title:** Dashboard total content count includes all users' content

**Severity:** High
**Domain:** Dashboard
**Component:** `dashboard/services.py`

### Description
The `total_contents` statistic on the dashboard uses `Content.objects.count()` (global count) instead of filtering by the current user. On a multi-user instance, the number shown is the total of all users' content across the entire database.

### Steps to reproduce
1. Create two user accounts: User A (3 items) and User B (2 items)
2. Log in as User A
3. Navigate to `/dashboard/`
4. Observe: "Total" shows 5 (User A's 3 + User B's 2)

### Expected behavior
Total should show 3 (User A's items only).

### Actual behavior
Total shows the sum of all users' content.

### Code change
```python
# dashboard/services.py — total_contents uses Content.objects.count() instead of Content.objects.filter(user=user).count()
```

---

## B-16

**Title:** "Generate Description" button populates the title field instead of the description field

**Severity:** Medium
**Domain:** AI / UI
**Component:** `templates/contents/content_form.html` (JavaScript)
**Test coverage:** Browser testing required

### Description
In the content form, clicking "✨ AI Generate" (Generate Description) triggers an AJAX call and receives an AI-generated description. However, the JavaScript success handler writes the result to `#id_title` instead of `#id_description`. The user's title is overwritten with the AI-generated description, and the description field remains empty.

### Steps to reproduce
1. Navigate to `/contents/create/`
2. Type a title such as "Python async/await tutorial"
3. Click the "✨ AI Generate" button (for description)
4. Observe: the title field is overwritten with the AI text; the description field remains empty

### Expected behavior
The description field is populated with the AI-generated text; title is untouched.

### Actual behavior
The title field is overwritten with the AI text.

### Code change
```javascript
// content_form.html — success handler writes to document.getElementById('id_title') instead of 'id_description'
```

---

## B-17

**Title:** Successful content creation displays the flash message with error (red) styling

**Severity:** Low
**Domain:** UI
**Component:** `contents/views.py` — `ContentCreateView`

### Description
After successfully creating a content item, the flash message text says "Content created successfully!" but it is rendered with error-level styling (red/danger color scheme). The message is technically correct but its colour communicates an error state to the user.

### Steps to reproduce
1. Navigate to `/contents/create/`
2. Fill in the required fields (URL or title, content type)
3. Submit the form
4. Observe: the content is saved, but the flash message banner appears in red

### Expected behavior
Flash message uses success styling (green/emerald color scheme).

### Actual behavior
Flash message uses error styling (red/rose color scheme).

### Code change
```python
# contents/views.py — ContentCreateView.form_valid calls messages.error() instead of messages.success()
```

---

## B-18

**Title:** Sidebar "Contents" link navigates to the Categories page

**Severity:** Medium
**Domain:** UI / Navigation
**Component:** `templates/components/sidebar.html`
**Test coverage:** Browser testing required

### Description
The "Contents" navigation item in the sidebar has its `href` pointing to `{% url 'categories:list' %}` instead of `{% url 'contents:list' %}`. The label and icon correctly say "Contents", but clicking the link navigates to the Categories page.

### Steps to reproduce
1. Log in and navigate to any authenticated page
2. Click the "Contents" link in the left sidebar
3. Observe: the page navigates to `/categories/` instead of `/contents/`

### Expected behavior
Clicking "Contents" navigates to `/contents/`.

### Actual behavior
Navigates to `/categories/`.

### Code change
```html
<!-- sidebar.html — href changed from url 'contents:list' to url 'categories:list' -->
```

---

## B-19

**Title:** AI "Suggest Category" uses categories from all users, not just the current user

**Severity:** High
**Domain:** AI / Data Isolation
**Component:** `insights/views.py` — `SuggestCategoryView`

### Description
The `SuggestCategoryView` fetches all categories from all users (`Category.objects.all()`) to build the prompt for the AI suggestion. The AI may suggest a category name that belongs to another user. Since that category is not in the current user's dropdown, the suggestion either silently fails to match or — if the frontend dynamically creates the option — saves the content with a cross-user category reference.

### Steps to reproduce
1. Log in as User A (categories: "Frontend", "Testing")
2. Log in as User B in another session (categories: "DevOps", "Security")
3. As User A, create a new content item with title "Kubernetes cluster setup"
4. After URL or title blur, observe the AI-suggested category
5. The AI may suggest "DevOps" (User B's category) which does not appear in User A's dropdown

### Expected behavior
AI should only consider the current user's categories when making suggestions.

### Actual behavior
AI receives all categories from all users; may suggest another user's private category.

### Code change
```python
# insights/views.py — Category.objects.filter(user=request.user) changed to Category.objects.all()
```

---

## B-20

**Title:** "Generate Insights" renders AI HTML response unsanitized — potential stored XSS

**Severity:** High
**Domain:** AI / Security
**Component:** `insights/services.py`, `templates/insights/index.html` (JavaScript)
**Test coverage:** Browser testing required

### Description
The AI prompt for `generate_insights` now explicitly requests HTML-formatted output (`<ul>`, `<li>`, `<strong>` tags). The JavaScript handler in the insights panel renders the response using `innerHTML` without any sanitization. Because the AI context includes the user's content titles, a user who creates a content item with a title containing an HTML/script payload can influence the AI output and inject that payload into the DOM when the insights panel renders.

### Steps to reproduce
1. Create a content item with title `<img src=x onerror=alert('XSS')>`
2. Navigate to `/insights/`
3. Click "Generate Insights"
4. Observe: the browser renders the unsanitized HTML; the injected tag/script executes in the browser

### Expected behavior
AI output should be sanitized or rendered as text; user-controlled data should never reach `innerHTML` unsanitized.

### Actual behavior
AI-generated HTML (including content influenced by user input) is rendered via `innerHTML` — XSS vector.

### Code change
```python
# insights/services.py — generate_insights prompt instructs AI to return HTML-formatted output
# templates/insights/index.html — JS handler uses innerHTML for rendering
```

---

## Test Verification Summary

| Bug ID | Verification method | Test class | Pass when bug present |
|--------|--------------------|-----------|-----------------------|
| B-01 | `users.BugVerificationTests.test_bug_10_1_1_short_password_accepted` | Automated | ✅ |
| B-02 | `users.BugVerificationTests.test_bug_10_1_2_login_reveals_email_existence` | Automated | ✅ |
| B-03 | `users.BugVerificationTests.test_bug_10_1_3_password_change_invalidates_session` | Automated | ✅ |
| B-04 | `contents.ContentCreateTest.test_missing_title_shows_form_error_no_content_saved` | Sprint 9 (now fails) | ✅ |
| B-05 | `contents.ContentFilteringTest.test_filter_by_status_*` | Sprint 9 (now fails) | ✅ |
| B-06 | `contents.ContentDataIsolationTest.test_user_a_cannot_access_user_b_edit` | Sprint 9 (now fails) | ✅ |
| B-07 | `contents.BugVerificationTests.test_bug_10_1_7_oldest_sort_same_as_newest` | Automated | ✅ |
| B-08 | `contents.BugVerificationTests.test_bug_10_1_8_mark_completed_saves_in_progress` | Automated | ✅ |
| B-09 | `contents.BugVerificationTests.test_bug_10_1_9_total_count_ignores_filter` | Automated | ✅ |
| B-10 | `categories.CategoryCRUDTest.test_delete_category_removes_it_and_nullifies_content_category` | Sprint 9 (now errors) | ✅ |
| B-11 | `categories.CategoryDuplicateNameTest.test_duplicate_category_name_*` | Sprint 9 (now fails) | ✅ |
| B-12 | `tags.BugVerificationTests.test_bug_10_1_12_tag_content_count_always_zero` | Automated | ✅ |
| B-13 | `tags.TagCRUDTest.test_delete_tag_removes_it_and_content_not_deleted` | Sprint 9 (now fails) | ✅ |
| B-14 | `dashboard.DashboardRecentListsTest.test_recently_completed_*` | Sprint 9 (now fails) | ✅ |
| B-15 | `dashboard.BugVerificationTests.test_bug_10_1_15_total_count_includes_all_users` | Automated | ✅ |
| B-16 | Manual / browser | — | 🌐 |
| B-17 | `contents.BugVerificationTests.test_bug_10_1_17_create_content_uses_error_message` | Automated | ✅ |
| B-18 | Manual / browser | — | 🌐 |
| B-19 | `insights.BugVerificationTests.test_bug_10_1_19_suggest_category_uses_all_categories` | Automated | ✅ |
| B-20 | Manual / browser | — | 🌐 |
