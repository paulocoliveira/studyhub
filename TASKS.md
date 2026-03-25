## Task List — Sprints

### Sprint 1: Project Setup & Authentication

> **Goal:** Initialize the Django project, set up TailwindCSS, create the custom user model with email-based auth, and build the landing page.

- [X] **1.1 — Initialize Django Project**
  - [X] 1.1.1 — Create a new Django project named `studyhub` with `core` as the settings module (`django-admin startproject core .`)
  - [X] 1.1.2 — Configure `core/settings.py`: set `AUTH_USER_MODEL`, `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`, default language to `en-us`, timezone, static files configuration
  - [X] 1.1.3 — Create the directory structure for templates: `templates/`, `templates/components/`, `templates/users/`, `templates/dashboard/`, `templates/contents/`, `templates/categories/`, `templates/tags/`, `templates/insights/`
  - [X] 1.1.4 — Create `static/` directory structure: `static/css/`, `static/js/`, `static/images/`
  - [X] 1.1.5 — Configure `core/urls.py` with the root URL patterns including `admin/` and placeholder includes for all apps

- [X] **1.2 — Set Up TailwindCSS**
  - [X] 1.2.1 — Add TailwindCSS via CDN in the base template `<head>` tag with the Inter font from Google Fonts
  - [X] 1.2.2 — Configure the TailwindCSS `tailwind.config` inline script in the base template to extend the default theme with custom colors if needed

- [X] **1.3 — Create Base Templates**
  - [X] 1.3.1 — Create `templates/base_public.html`: HTML5 boilerplate, TailwindCSS CDN, Inter font, dark background (`bg-gray-950`), responsive meta viewport, block `title`, block `content`
  - [X] 1.3.2 — Create `templates/base.html`: extends structure with sidebar navigation, top bar with user info and logout, flash messages area, block `title`, block `content`. Sidebar includes nav links to: Dashboard, Contents, Categories, Tags, Insights
  - [X] 1.3.3 — Create `templates/components/sidebar.html`: reusable sidebar component with navigation items, active state handling using `{% url %}` and current path comparison
  - [X] 1.3.4 — Create `templates/components/topbar.html`: top bar with page title block, user email display, and logout button
  - [X] 1.3.5 — Create `templates/components/messages.html`: reusable flash messages component styled with success/error/warning/info variants

- [X] **1.4 — Create Users App & Custom User Model**
  - [X] 1.4.1 — Create the `users` app: `python manage.py startapp users`
  - [X] 1.4.2 — Define `CustomUser` model in `users/models.py`: extend `AbstractBaseUser` and `PermissionsMixin`, use email as `USERNAME_FIELD`, add `first_name`, `last_name`, `is_active`, `is_staff`, `created_at`, `updated_at` fields. Create `CustomUserManager` with `create_user` and `create_superuser` methods
  - [X] 1.4.3 — Register `CustomUser` in `users/admin.py` with `UserAdmin` customization for email-based display
  - [X] 1.4.4 — Create and run migrations for the `users` app
  - [ ] 1.4.5 — Create a superuser for admin access

- [X] **1.5 — Build Authentication Views**
  - [X] 1.5.1 — Create `users/forms.py` with `CustomUserCreationForm` (fields: email, first_name, last_name, password1, password2) and `EmailAuthenticationForm` (overriding `AuthenticationForm` to use email)
  - [X] 1.5.2 — Create `RegisterView` in `users/views.py`: CBV using `CreateView` with `CustomUserCreationForm`, redirects to login on success with a success message
  - [X] 1.5.3 — Create `CustomLoginView` in `users/views.py`: CBV extending `LoginView` with `EmailAuthenticationForm`, redirects to dashboard on success
  - [X] 1.5.4 — Create `CustomLogoutView` in `users/views.py`: CBV extending `LogoutView`, redirects to landing page
  - [X] 1.5.5 — Create `CustomPasswordChangeView` in `users/views.py`: CBV extending `PasswordChangeView`, redirects to dashboard with success message
  - [X] 1.5.6 — Configure `users/urls.py` with URL patterns: `register/`, `login/`, `logout/`, `password-change/`
  - [X] 1.5.7 — Include `users.urls` in `core/urls.py`

- [X] **1.6 — Build Authentication Templates**
  - [X] 1.6.1 — Create `templates/users/register.html`: registration form page extending `base_public.html`, styled with design system (dark card, gradient accents, form inputs per design system spec)
  - [X] 1.6.2 — Create `templates/users/login.html`: login form page extending `base_public.html`, matching registration page design, with link to register
  - [X] 1.6.3 — Create `templates/users/password_change.html`: password change form extending `base.html` (authenticated layout)

- [X] **1.7 — Build Landing Page**
  - [X] 1.7.1 — Create `LandingPageView` in `core/views.py` (or a dedicated view): simple `TemplateView` that renders the landing page. If user is authenticated, redirect to dashboard
  - [X] 1.7.2 — Create `templates/landing.html`: extends `base_public.html`. Hero section with gradient text title, subtitle, and CTA buttons (Sign Up, Log In). Features section with 3–4 feature cards. Footer with basic info
  - [X] 1.7.3 — Wire the landing page as the root URL `/` in `core/urls.py`

---

### Sprint 2: Categories & Tags

> **Goal:** Build the Categories and Tags apps with full CRUD and user-scoped data.

- [X] **2.1 — Create Categories App**
  - [X] 2.1.1 — Create the `categories` app: `python manage.py startapp categories`
  - [X] 2.1.2 — Define `Category` model in `categories/models.py`: fields `name` (CharField, max_length=100), `description` (TextField, blank=True), `user` (ForeignKey to `settings.AUTH_USER_MODEL`), `created_at`, `updated_at`. Add `Meta` with `unique_together = ['name', 'user']` and `ordering = ['name']`
  - [X] 2.1.3 — Register `Category` in `categories/admin.py`
  - [X] 2.1.4 — Create and run migrations for the `categories` app

- [X] **2.2 — Build Category Views**
  - [X] 2.2.1 — Create `categories/forms.py` with `CategoryForm` (ModelForm, fields: name, description)
  - [X] 2.2.2 — Create `CategoryListView` in `categories/views.py`: CBV using `ListView`, filtered by `request.user`, annotated with content count, `LoginRequiredMixin`
  - [X] 2.2.3 — Create `CategoryCreateView` in `categories/views.py`: CBV using `CreateView`, auto-assign `user` in `form_valid`, `LoginRequiredMixin`
  - [X] 2.2.4 — Create `CategoryUpdateView` in `categories/views.py`: CBV using `UpdateView`, restrict queryset to user's categories, `LoginRequiredMixin`
  - [X] 2.2.5 — Create `CategoryDeleteView` in `categories/views.py`: CBV using `DeleteView`, restrict queryset to user's categories, `LoginRequiredMixin`
  - [X] 2.2.6 — Configure `categories/urls.py` with URL patterns: list (`''`), create (`'create/'`), update (`'<int:pk>/edit/'`), delete (`'<int:pk>/delete/'`)
  - [X] 2.2.7 — Include `categories.urls` in `core/urls.py` under `categories/` prefix

- [X] **2.3 — Build Category Templates**
  - [X] 2.3.1 — Create `templates/categories/category_list.html`: list page extending `base.html`, shows categories in card grid with name, description, content count, edit/delete action buttons
  - [X] 2.3.2 — Create `templates/categories/category_form.html`: create/edit form page extending `base.html`, reusable for both create and update
  - [X] 2.3.3 — Create `templates/categories/category_confirm_delete.html`: delete confirmation page extending `base.html`

- [X] **2.4 — Create Tags App**
  - [X] 2.4.1 — Create the `tags` app: `python manage.py startapp tags`
  - [X] 2.4.2 — Define `Tag` model in `tags/models.py`: fields `name` (CharField, max_length=50), `user` (ForeignKey to `settings.AUTH_USER_MODEL`), `created_at`, `updated_at`. Add `Meta` with `unique_together = ['name', 'user']` and `ordering = ['name']`
  - [X] 2.4.3 — Register `Tag` in `tags/admin.py`
  - [X] 2.4.4 — Create and run migrations for the `tags` app

- [X] **2.5 — Build Tag Views**
  - [X] 2.5.1 — Create `tags/forms.py` with `TagForm` (ModelForm, fields: name)
  - [X] 2.5.2 — Create `TagListView` in `tags/views.py`: CBV using `ListView`, filtered by `request.user`, annotated with content count, `LoginRequiredMixin`
  - [X] 2.5.3 — Create `TagCreateView` in `tags/views.py`: CBV using `CreateView`, auto-assign `user` in `form_valid`, `LoginRequiredMixin`
  - [X] 2.5.4 — Create `TagDeleteView` in `tags/views.py`: CBV using `DeleteView`, restrict queryset to user's tags, `LoginRequiredMixin`
  - [X] 2.5.5 — Configure `tags/urls.py` with URL patterns: list (`''`), create (`'create/'`), delete (`'<int:pk>/delete/'`)
  - [X] 2.5.6 — Include `tags.urls` in `core/urls.py` under `tags/` prefix

- [X] **2.6 — Build Tag Templates**
  - [X] 2.6.1 — Create `templates/tags/tag_list.html`: list page extending `base.html`, shows tags in a compact grid/list with name, content count, and delete action
  - [X] 2.6.2 — Create `templates/tags/tag_form.html`: create form page extending `base.html`
  - [X] 2.6.3 — Create `templates/tags/tag_confirm_delete.html`: delete confirmation page extending `base.html`

---

### Sprint 3: Content Management

> **Goal:** Build the Contents app with full CRUD, filtering, search, and sorting.

- [X] **3.1 — Create Contents App**
  - [X] 3.1.1 — Create the `contents` app: `python manage.py startapp contents`
  - [X] 3.1.2 — Define `Content` model in `contents/models.py`: fields `title` (CharField, max_length=255), `url` (URLField, blank=True), `content_type` (CharField with choices), `description` (TextField, blank=True), `status` (CharField with choices, default='new'), `user` (ForeignKey to `settings.AUTH_USER_MODEL`), `category` (ForeignKey to `Category`, null=True, blank=True), `tags` (ManyToManyField to `Tag`, blank=True), `created_at`, `updated_at`. Add `Meta` with `ordering = ['-created_at']`
  - [X] 3.1.3 — Define `CONTENT_TYPE_CHOICES` and `STATUS_CHOICES` as module-level constants in `contents/models.py`
  - [X] 3.1.4 — Register `Content` in `contents/admin.py` with list display, list filter, and search fields
  - [X] 3.1.5 — Create and run migrations for the `contents` app

- [X] **3.2 — Build Content Forms**
  - [X] 3.2.1 — Create `contents/forms.py` with `ContentForm` (ModelForm, fields: title, url, content_type, description, category, tags, status). Override `__init__` to filter category and tags querysets by `self.user`
  - [X] 3.2.2 — Create `ContentFilterForm` in `contents/forms.py`: a simple `Form` (not ModelForm) with optional fields for status, content_type, category (filtered by user), and a search text field, used for filtering the content list

- [X] **3.3 — Build Content Views**
  - [X] 3.3.1 — Create `ContentListView` in `contents/views.py`: CBV using `ListView`, filtered by `request.user`, supports filtering by status, content_type, category, and tag via GET parameters. Supports text search via `Q` objects on title and description. Supports sorting via GET parameter. Uses `ContentFilterForm` in context. Add pagination (12 items per page)
  - [X] 3.3.2 — Create `ContentDetailView` in `contents/views.py`: CBV using `DetailView`, restrict queryset to user's content
  - [X] 3.3.3 — Create `ContentCreateView` in `contents/views.py`: CBV using `CreateView`, auto-assign `user` in `form_valid`, pass `user` to form `__init__`
  - [X] 3.3.4 — Create `ContentUpdateView` in `contents/views.py`: CBV using `UpdateView`, restrict queryset to user's content, pass `user` to form `__init__`
  - [X] 3.3.5 — Create `ContentDeleteView` in `contents/views.py`: CBV using `DeleteView`, restrict queryset to user's content
  - [X] 3.3.6 — Create `ContentStatusUpdateView` in `contents/views.py`: CBV (or function view) that accepts a POST request to update only the status of a content item. Returns redirect back to referer or content list
  - [X] 3.3.7 — Configure `contents/urls.py` with URL patterns: list (`''`), create (`'create/'`), detail (`'<int:pk>/'`), update (`'<int:pk>/edit/'`), delete (`'<int:pk>/delete/'`), status-update (`'<int:pk>/status/'`)
  - [X] 3.3.8 — Include `contents.urls` in `core/urls.py` under `contents/` prefix

- [X] **3.4 — Build Content Templates**
  - [X] 3.4.1 — Create `templates/contents/content_list.html`: list page extending `base.html`. Includes filter sidebar/bar with `ContentFilterForm` (status, type, category dropdowns + search input). Content displayed as card grid with: title, type badge, status badge, category name, date added, and quick status change buttons. Pagination controls at the bottom
  - [X] 3.4.2 — Create `templates/contents/content_detail.html`: detail page extending `base.html`. Shows all content fields. Action buttons: edit, delete, change status. External link to URL if present. Shows associated tags as badges
  - [X] 3.4.3 — Create `templates/contents/content_form.html`: create/edit form page extending `base.html`. All form fields styled per design system. AI action buttons placeholder (wired in Sprint 5). Tag multi-select field
  - [X] 3.4.4 — Create `templates/contents/content_confirm_delete.html`: delete confirmation page extending `base.html`
  - [X] 3.4.5 — Create `templates/components/pagination.html`: reusable pagination component showing page numbers, previous/next buttons, styled per design system

---

### Sprint 4: Dashboard

> **Goal:** Build the Dashboard app with aggregated stats and recent activity.

- [X] **4.1 — Create Dashboard App**
  - [X] 4.1.1 — Create the `dashboard` app directory structure (it doesn't need migrations as it has no models): `dashboard/__init__.py`, `dashboard/views.py`, `dashboard/services.py`
  - [X] 4.1.2 — Register the `dashboard` app in `INSTALLED_APPS`

- [X] **4.2 — Build Dashboard Service Layer**
  - [X] 4.2.1 — Create `dashboard/services.py` with a `DashboardService` class (or functions) that computes:
    - Total content count for the user
    - Content count by status (new, in_progress, completed)
    - Content count by content type
    - 5 most recently added content items
    - 5 most recently completed content items (filtered by status='completed', ordered by `updated_at`)
    - Top 5 categories by content count
    - Top 5 tags by content count
  - [X] 4.2.2 — Use Django ORM aggregations (`Count`, `annotate`) for efficient queries

- [X] **4.3 — Build Dashboard View**
  - [X] 4.3.1 — Create `DashboardView` in `dashboard/views.py`: CBV using `TemplateView`, `LoginRequiredMixin`. Override `get_context_data` to call `DashboardService` and pass all stats to the template

- [X] **4.4 — Build Dashboard Template**
  - [X] 4.4.1 — Create `templates/dashboard/dashboard.html`: extending `base.html`. Layout:
    - **Row 1:** Stats cards grid (total contents, new, in progress, completed) with colored accents per status
    - **Row 2:** Content type breakdown (compact list or small cards showing count per type)
    - **Row 3:** Two columns — "Recently Added" (list of 5 items with title, type, date) and "Recently Completed" (list of 5 items with title, type, completion date)
    - **Row 4:** Two columns — "Top Categories" (list with name + count) and "Top Tags" (list with name + count)
  - [X] 4.4.2 — Configure `dashboard/urls.py` with a single URL pattern: `''` → `DashboardView`
  - [X] 4.4.3 — Include `dashboard.urls` in `core/urls.py` under `dashboard/` prefix
  - [X] 4.4.4 — Update `LOGIN_REDIRECT_URL` in settings to point to the dashboard URL

---

### Sprint 5: AI Insights

> **Goal:** Integrate AI features for category suggestion, description generation, and consumption insights.

- [X] **5.1 — Create Insights App**
  - [X] 5.1.1 — Create the `insights` app: `python manage.py startapp insights`
  - [X] 5.1.2 — Install the `anthropic` Python SDK: add to `requirements.txt`
  - [X] 5.1.3 — Add `ANTHROPIC_API_KEY` setting in `core/settings.py` (read from environment variable)
  - [X] 5.1.4 — Register the `insights` app in `INSTALLED_APPS`

- [X] **5.2 — Build AI Service Layer**
  - [X] 5.2.1 — Create `insights/services.py` with an `AIService` class containing:
    - `suggest_category(title, url, user_categories)`: sends a prompt to Claude API asking for the best category from the user's existing categories (returns category name string)
    - `generate_description(title, url, content_type)`: sends a prompt to Claude API asking for a short description of the content (returns description string)
    - `generate_insights(user_stats)`: sends a prompt to Claude API with the user's content statistics and asks for a brief analysis of their consumption habits and suggestions (returns markdown/text string)
  - [X] 5.2.2 — Implement proper error handling in `AIService`: catch API errors, timeouts, and return `None` or a user-friendly error message
  - [X] 5.2.3 — Implement rate limiting logic: simple in-memory or session-based check to prevent excessive API calls per user per day

- [X] **5.3 — Build AI API Views**
  - [X] 5.3.1 — Create `SuggestCategoryView` in `insights/views.py`: accepts POST with `title` and `url`, calls `AIService.suggest_category`, returns JSON response. `LoginRequiredMixin`
  - [X] 5.3.2 — Create `GenerateDescriptionView` in `insights/views.py`: accepts POST with `title`, `url`, and `content_type`, calls `AIService.generate_description`, returns JSON response. `LoginRequiredMixin`
  - [X] 5.3.3 — Create `GenerateInsightsView` in `insights/views.py`: accepts GET, gathers user stats via `DashboardService`, calls `AIService.generate_insights`, returns rendered HTML or JSON. `LoginRequiredMixin`
  - [X] 5.3.4 — Configure `insights/urls.py` with URL patterns: `suggest-category/`, `generate-description/`, `generate-insights/`
  - [X] 5.3.5 — Include `insights.urls` in `core/urls.py` under `insights/` prefix

- [X] **5.4 — Integrate AI into Content Form**
  - [X] 5.4.1 — Add JavaScript to `templates/contents/content_form.html`: an "AI Suggest Category" button that sends an AJAX POST to `suggest-category/` endpoint with the current title and URL fields, and populates the category dropdown on success
  - [X] 5.4.2 — Add JavaScript to `templates/contents/content_form.html`: an "AI Generate Description" button that sends an AJAX POST to `generate-description/` endpoint with current title, URL, and content_type fields, and populates the description textarea on success
  - [X] 5.4.3 — Style the AI buttons distinctively (e.g., small gradient buttons with a sparkle/AI icon) so they are clearly identified as AI features
  - [X] 5.4.4 — Add loading states (spinner/disabled button) while AI requests are in progress
  - [X] 5.4.5 — Add error handling UI: show a toast or inline message if the AI call fails

- [X] **5.5 — Build Insights Dashboard Section**
  - [X] 5.5.1 — Create `templates/insights/insights_panel.html`: a panel/card that can be included in the dashboard or shown as a standalone page. Contains a "Generate Insights" button and an area to display the AI-generated text
  - [X] 5.5.2 — Add JavaScript to the insights panel: clicking the button sends AJAX GET to `generate-insights/`, displays the result in the panel with loading state
  - [X] 5.5.3 — Integrate the insights panel into the dashboard template (add as a new row or section at the bottom of the dashboard)

---

### Sprint 6: Polish & Refinements

> **Goal:** Improve UX, fix edge cases, add responsive refinements, and ensure design consistency.

- [X] **6.1 — Responsive Design Audit**
  - [X] 6.1.1 — Test all pages at mobile viewport (375px) and fix layout issues: sidebar collapses to hamburger menu, forms stack vertically, cards go single column
  - [X] 6.1.2 — Test all pages at tablet viewport (768px) and fix: 2-column grids, proper spacing
  - [X] 6.1.3 — Add mobile sidebar toggle: hamburger icon in top bar, sidebar slides in as overlay on mobile, close on backdrop click or navigation

- [X] **6.2 — Empty States**
  - [X] 6.2.1 — Add empty state UI to content list when no items exist: illustration/icon + "No content saved yet" message + CTA button to add first content
  - [X] 6.2.2 — Add empty state UI to categories list when no categories exist
  - [X] 6.2.3 — Add empty state UI to tags list when no tags exist
  - [X] 6.2.4 — Add empty state UI to dashboard when user has no content: welcome message + suggested first steps

- [X] **6.3 — Flash Messages & Feedback**
  - [X] 6.3.1 — Ensure all CRUD operations trigger appropriate Django messages (success on create/edit/delete, error on failure)
  - [X] 6.3.2 — Add auto-dismiss behavior to flash messages (fade out after 5 seconds) via JavaScript
  - [X] 6.3.3 — Add confirmation modals for delete actions (replace the separate confirmation page with an inline modal if desired, or keep as-is for simplicity)

- [X] **6.4 — Navigation Enhancements**
  - [X] 6.4.1 — Highlight the active sidebar link based on the current URL path
  - [X] 6.4.2 — Add breadcrumbs to detail and form pages (e.g., Contents > Content Title > Edit)
  - [X] 6.4.3 — Add a "Back" link to all form and detail pages

- [X] **6.5 — Content Form UX**
  - [X] 6.5.1 — Add tag input as a multi-select with checkboxes or a tag-picker component (using simple JS or Django widget)
  - [X] 6.5.2 — Add client-side form validation feedback (required fields highlighted before submit)
  - [X] 6.5.3 — Auto-detect content type from URL if possible (e.g., YouTube URL → video, Instagram URL → social_media_post) using simple JavaScript regex matching

- [X] **6.6 — Design Consistency Review**
  - [X] 6.6.1 — Audit all templates against the design system: verify color usage, button styles, input styles, typography, spacing, and border radius are consistent
  - [X] 6.6.2 — Ensure all pages use the same card style, badge style, and grid patterns
  - [X] 6.6.3 — Verify gradient usage is consistent (hero, buttons, accents)

---

### Sprint 7: Content Cards View, Link Previews & File Upload Security

> **Goal:** Add a card-based view for content with link preview thumbnails (Open Graph images), placeholder images per content type, and enforce file upload restrictions for security (allowed formats and 10MB size limit).

- [X] **7.1 — Link Preview Metadata Extraction**
  - [X] 7.1.1 — Install `requests` and `beautifulsoup4` packages and add them to `requirements.txt`
  - [X] 7.1.2 — Create a `contents/services.py` file (or extend if it already exists) with a `LinkPreviewService` class containing a method `fetch_preview(url: str) -> dict` that: sends a GET request to the URL with a timeout of 5 seconds, parses the HTML response with BeautifulSoup, extracts Open Graph metadata (`og:image`, `og:title`, `og:description`), and returns a dictionary with keys `preview_image_url`, `og_title`, `og_description`. If the request fails or no OG image is found, return `None` values gracefully
  - [X] 7.1.3 — Add error handling in `LinkPreviewService`: catch `requests.RequestException`, `Timeout`, `ConnectionError`, and invalid URLs. Return empty/null preview data on failure — never crash the content save flow
  - [X] 7.1.4 — Add a `preview_image_url` field (URLField, blank=True, max_length=500) to the `Content` model to store the fetched Open Graph image URL. Create and run the migration

- [X] **7.2 — Auto-Fetch Preview on Content Save**
  - [X] 7.2.1 — Create `contents/signals.py` with a `pre_save` signal on the `Content` model: if the content has a `url` value and `preview_image_url` is empty, call `LinkPreviewService.fetch_preview(url)` and populate `preview_image_url` with the result. Only trigger on creation or when `url` has changed
  - [X] 7.2.2 — Register the signal in `contents/apps.py` inside the `ready()` method
  - [X] 7.2.3 — Add a manual "Refresh Preview" button on the content edit form that triggers an AJAX POST to a new endpoint `contents/<int:pk>/refresh-preview/` which re-fetches the OG image and updates the field. Return JSON with the new `preview_image_url`

- [X] **7.3 — Content Type Placeholder Images**
  - [X] 7.3.1 — Create or source 7 placeholder SVG icons (one per content type: article, video, podcast, book, course, tool, other)
  - [X] 7.3.2 — Save the placeholder SVGs in `static/images/placeholders/`
  - [X] 7.3.3 — Create a model method `get_card_image()` on the `Content` model

- [X] **7.4 — Content Card Component & Grid View**
  - [X] 7.4.1 — Create `templates/components/content_card.html`: reusable card component
  - [X] 7.4.2 — Image area with `onerror` fallback to placeholder SVG
  - [X] 7.4.3 — Update `templates/contents/content_list.html`: view toggle (grid/list), default cards, localStorage persistence
  - [X] 7.4.4 — View toggle JavaScript with localStorage persistence

- [X] **7.5 — File Upload Model & Validation**
  - [X] 7.5.1 — Add optional `file` field (FileField) to `Content` model with migration
  - [X] 7.5.2 — Create `contents/validators.py` with `validate_file_extension` and `validate_file_size`
  - [X] 7.5.3 — Apply both validators to the `file` field on the `Content` model
  - [X] 7.5.4 — Add `ALLOWED_UPLOAD_EXTENSIONS` and `MAX_UPLOAD_SIZE_MB` constants to `core/settings.py`
  - [X] 7.5.5 — Configure `MEDIA_URL`, `MEDIA_ROOT`, and media URL patterns in `core/urls.py`

- [X] **7.6 — File Upload Form Integration**
  - [X] 7.6.1 — Update `ContentForm` with `file` field; add `enctype="multipart/form-data"` to form tag
  - [X] 7.6.2 — Client-side file validation JS (extension + size check, inline error, disable submit)
  - [X] 7.6.3 — Helper text below file input: accepted formats and max size
  - [X] 7.6.4 — Download link on content detail page when file is present

- [X] **7.7 — Card Image Handling for Uploaded Files**
  - [X] 7.7.1 — `get_card_image()` method: uploaded image → OG preview → placeholder SVG priority chain
  - [X] 7.7.2 — Non-image uploads fall back to content type placeholder (PDF, audio, video)

---

### Sprint 8: Testing

> **Goal:** Add automated tests for critical functionality.

- [ ] **8.1 — User Authentication Tests**
  - [ ] 8.1.1 — Write tests in `users/tests.py` for: user registration with valid data succeeds, registration with duplicate email fails, registration with mismatched passwords fails
  - [ ] 8.1.2 — Write tests for: login with correct email/password succeeds, login with wrong password fails, login with non-existent email fails
  - [ ] 8.1.3 — Write tests for: authenticated user can access dashboard, unauthenticated user is redirected to login

- [ ] **8.2 — Content CRUD Tests**
  - [ ] 8.2.1 — Write tests in `contents/tests.py` for: creating content with valid data, creating content with missing required fields fails
  - [ ] 8.2.2 — Write tests for: user can only see their own content, user cannot access another user's content detail/edit/delete
  - [ ] 8.2.3 — Write tests for: content status update works correctly, content deletion works correctly
  - [ ] 8.2.4 — Write tests for: content list filtering by status, type, and category returns correct results
  - [ ] 8.2.5 — Write tests for: content list search returns correct results

- [ ] **8.3 — Category & Tag Tests**
  - [ ] 8.3.1 — Write tests in `categories/tests.py` for: category CRUD operations, user scoping (user A cannot see/edit user B's categories)
  - [ ] 8.3.2 — Write tests in `tags/tests.py` for: tag CRUD operations, user scoping, duplicate tag name per user fails

- [ ] **8.4 — Dashboard Tests**
  - [ ] 8.4.1 — Write tests in `dashboard/tests.py` for: dashboard loads for authenticated user, stats are correctly calculated (create test data and verify counts)

- [ ] **8.5 — AI Service Tests**
  - [ ] 8.5.1 — Write tests in `insights/tests.py` for: AI views return proper JSON responses (mock the API calls), AI views require authentication, error handling when API fails

---

### Sprint 9: Bug Injection — QA Hackathon

> **Goal:** Intentionally introduce 18 bugs across the application for a QA hackathon challenge. Participants must explore and test the application to discover and document these defects. Bugs span multiple severity levels (critical, major, minor, cosmetic) and multiple domains (auth, content, categories, tags, dashboard, AI, UI/UX) to reward diverse testing strategies.

- [ ] **9.1 — Inject Bugs into the Application**

  - [ ] 9.1.1 — **Auth: Registration accepts passwords shorter than 8 characters.** Remove or bypass Django's `MinimumLengthValidator` in `AUTH_PASSWORD_VALIDATORS` settings so users can register with extremely short passwords like "123" without any validation error.

  - [ ] 9.1.2 — **Auth: Login error message reveals whether the email exists.** Modify the `EmailAuthenticationForm` or `CustomLoginView` to show "Password is incorrect" when the email exists but the password is wrong, and "Email not found" when the email doesn't exist. This is an information disclosure vulnerability — the default Django behavior uses a generic message, so the bug is introduced by replacing it with specific messages.

  - [ ] 9.1.3 — **Auth: After changing password, user session is not invalidated.** Modify `CustomPasswordChangeView` to skip calling `update_session_auth_hash()` after a successful password change, causing the user to be logged out unexpectedly after the redirect. The success message says "Password changed successfully" but the user is kicked to the login page.

  - [ ] 9.1.4 — **Content: Creating content without a title silently saves with an empty title.** Remove the `required` constraint from the `title` field in `ContentForm` (set `required=False` and remove model-level blank validation or use `blank=True` on the model). The form submits successfully and the content list shows an empty-titled card.

  - [ ] 9.1.5 — **Content: Status filter shows all content regardless of selected status.** In `ContentListView`, introduce a bug in the filter logic: when the `status` GET parameter is present, use `.exclude(status=status)` instead of `.filter(status=status)`. This inverts the results — selecting "Completed" shows everything except completed items.

  - [ ] 9.1.6 — **Content: Editing content from another user is possible via direct URL manipulation.** In `ContentUpdateView`, remove the queryset filtering by `request.user` (remove the `get_queryset` override that limits to the logged-in user's content). Any authenticated user can now edit any content by navigating directly to `/contents/<other_user_content_id>/edit/`.

  - [ ] 9.1.7 — **Content: Sorting by "oldest first" still sorts by newest first.** In `ContentListView`, when the sort parameter is `oldest`, apply `.order_by('-created_at')` (descending) instead of `.order_by('created_at')` (ascending), making both "newest" and "oldest" sort options produce the same result.

  - [ ] 9.1.8 — **Content: Quick status change to "Completed" sets the status to "In Progress" instead.** In `ContentStatusUpdateView`, introduce a mapping bug: when the received status value is `completed`, save it as `in_progress` instead. The user clicks "Mark as Completed" but the badge changes to "In Progress".

  - [ ] 9.1.9 — **Content: Pagination shows wrong total count on filtered results.** In `ContentListView`, compute the `total_count` context variable using the unfiltered queryset (`Content.objects.filter(user=request.user).count()`) instead of the filtered queryset's count. When filters are active, the header says "Showing 47 contents" even though only 3 are displayed on the page.

  - [ ] 9.1.10 — **Categories: Deleting a category also deletes all content in that category.** On the `Category` model's `user` ForeignKey (or the Content model's `category` ForeignKey), change `on_delete=models.SET_NULL` to `on_delete=models.CASCADE`. When a user deletes a category, all content associated with that category is silently deleted instead of having its category set to null.

  - [ ] 9.1.11 — **Categories: Duplicate category names are allowed for the same user.** Remove the `unique_together = ['name', 'user']` constraint from the `Category` model's `Meta` class. Users can now create multiple categories with identical names, causing confusion in filters and dropdowns.

  - [ ] 9.1.12 — **Tags: Tag content count on the tag list page always shows 0.** In `TagListView`, introduce a bug in the annotation: use `Count('id')` instead of `Count('content')` (or reference a wrong related name), so the content count annotation always returns 0 for every tag regardless of how many contents are actually tagged.

  - [ ] 9.1.13 — **Tags: Deleting a tag does not remove it from associated content items.** Override the `Tag.delete()` method (or the `TagDeleteView`) to call `self.content_set.clear()` **after** `super().delete()` — since the tag is already deleted, the clear does nothing and orphan references remain. Alternatively, skip the M2M cleanup entirely so the through-table retains stale entries. This manifests as ghost tag badges on content detail pages that link to a 404.

  - [ ] 9.1.14 — **Dashboard: "Recently Completed" section shows recently added items instead.** In `DashboardService`, for the "recently completed" query, use `.order_by('-created_at')` instead of `.order_by('-updated_at')` and omit the `.filter(status='completed')`. This returns the most recently created items regardless of status, identical to the "Recently Added" section.

  - [ ] 9.1.15 — **Dashboard: Total content count includes content from all users.** In `DashboardService`, compute the total count with `Content.objects.count()` instead of `Content.objects.filter(user=user).count()`. On a multi-user instance, the total stat is inflated with other users' content while the per-status breakdown is correct (user-scoped), creating a mismatch.

  - [ ] 9.1.16 — **AI: "Generate Description" button populates the title field instead of the description field.** In the JavaScript on `content_form.html`, the AJAX success handler for the "Generate Description" button targets `#id_title` instead of `#id_description`, overwriting the user's title with the AI-generated description text.

  - [ ] 9.1.17 — **UI: Flash success message appears with error styling (red) on content creation.** In the `ContentCreateView`, use `messages.error()` instead of `messages.success()` when content is created. The message text says "Content created successfully!" but it renders with the red/danger color scheme, confusing the user.

  - [ ] 9.1.18 — **UI: Sidebar "Contents" link points to the categories page.** In `templates/components/sidebar.html`, set the `href` of the "Contents" navigation item to `{% url 'categories:list' %}` instead of `{% url 'contents:list' %}`. The icon and label say "Contents" but clicking it navigates to the categories page.

  - [ ] 9.1.19 — **AI: "Suggest Category" returns a category that does not belong to the user.** In `AIService.suggest_category`, pass the full list of all categories from the database (`Category.objects.all()`) instead of only the user's categories (`Category.objects.filter(user=user)`) to the AI prompt. The AI may suggest a category name that belongs to another user. When the AJAX success handler tries to match and select it in the dropdown, it either selects nothing (silent failure) or, if the frontend creates the option dynamically, saves the content with a reference to another user's category.

  - [ ] 9.1.20 — **AI: "Generate Insights" displays the raw markdown/HTML response without sanitization.** In `GenerateInsightsView`, return the AI-generated text and inject it into the DOM using `innerHTML` (in the JavaScript handler) without any sanitization or escaping. Additionally, modify the AI prompt in `AIService.generate_insights` to instruct the model to format the response with HTML tags (`<h3>`, `<ul>`, `<strong>`, etc.). Since the response is rendered unsanitized, if a user manages to influence the AI output (e.g., by having content titles with `<script>` tags), the raw HTML/script is rendered in the insights panel — a stored XSS vector.

- [ ] **9.2 — Manual Verification of Injected Bugs**

  - [ ] 9.2.1 — Create two test user accounts (e.g., `tester1@studyhub.com` and `tester2@studyhub.com`) with sample data: at least 15 content items each across different types, statuses, categories, and tags
  - [ ] 9.2.2 — Verify bug 9.1.1: attempt registration with a 2-character password → registration succeeds (should have been rejected)
  - [ ] 9.2.3 — Verify bug 9.1.2: attempt login with existing email + wrong password, then with non-existent email → different error messages are shown (should be the same generic message)
  - [ ] 9.2.4 — Verify bug 9.1.3: log in, change password, observe redirect → user is logged out and sent to login page instead of staying on the dashboard
  - [ ] 9.2.5 — Verify bug 9.1.4: create content leaving the title field empty → form submits and saves an untitled content item
  - [ ] 9.2.6 — Verify bug 9.1.5: apply "Completed" status filter on the content list → results show everything except completed items
  - [ ] 9.2.7 — Verify bug 9.1.6: log in as tester1, note the edit URL of one of tester1's content items (e.g., `/contents/5/edit/`). Log in as tester2, navigate directly to that URL → tester1's content is editable by tester2
  - [ ] 9.2.8 — Verify bug 9.1.7: sort content list by "oldest first" → results are in the same order as "newest first"
  - [ ] 9.2.9 — Verify bug 9.1.8: click "Mark as Completed" on a content item → status changes to "In Progress" instead
  - [ ] 9.2.10 — Verify bug 9.1.9: apply a filter that returns few results → total count in the header still shows the unfiltered total
  - [ ] 9.2.11 — Verify bug 9.1.10: create a category with content, delete the category → all content in that category is also deleted
  - [ ] 9.2.12 — Verify bug 9.1.11: create two categories with the exact same name → both are saved without error
  - [ ] 9.2.13 — Verify bug 9.1.12: view the tag list page → all tags show "0 contents" even those with tagged content
  - [ ] 9.2.14 — Verify bug 9.1.13: delete a tag that is assigned to content → content detail still shows the deleted tag as a broken badge/link
  - [ ] 9.2.15 — Verify bug 9.1.14: mark several items as completed → "Recently Completed" section shows recently created items regardless of status
  - [ ] 9.2.16 — Verify bug 9.1.15: log in as tester1 → total content count on the dashboard includes tester2's items
  - [ ] 9.2.17 — Verify bug 9.1.16: on the content form, enter a title, click "Generate Description" → title field is overwritten with the AI description
  - [ ] 9.2.18 — Verify bug 9.1.17: create new content → flash message says "Content created successfully!" but appears in red/danger styling
  - [ ] 9.2.19 — Verify bug 9.1.18: click "Contents" in the sidebar → user is navigated to the categories page instead
  - [ ] 9.2.20 — Verify bug 9.1.19: as tester1, create categories "AI" and "Career". As tester2, create categories "DevOps" and "Security". Log in as tester1, add new content with title "Kubernetes Best Practices", click "AI Suggest Category" → AI may suggest "DevOps" (tester2's category), which either fails to select in the dropdown or creates an invalid association
  - [ ] 9.2.21 — Verify bug 9.1.20: create a content item with title `<img src=x onerror=alert('XSS')>`. Navigate to the dashboard, click "Generate Insights" → the insights panel renders unsanitized HTML and the injected script/tag executes or renders in the browser
---

### Sprint 10: Deployment Preparation

> **Goal:** Prepare the project for production deployment with Docker and final configurations.

- [ ] **10.1 — Requirements & Dependencies**
  - [ ] 10.1.1 — Create `requirements.txt` with all project dependencies and pinned versions (Django, anthropic, gunicorn, etc.)
  - [ ] 10.1.2 — Create `.env.example` with all required environment variables: `SECRET_KEY`, `DEBUG`, `ANTHROPIC_API_KEY`, `ALLOWED_HOSTS`
  - [ ] 10.1.3 — Update `core/settings.py` to read all sensitive settings from environment variables using `os.environ`

- [ ] **10.2 — Docker Setup**
  - [ ] 10.2.1 — Create `Dockerfile`: Python 3.13 slim image, install dependencies, copy project, collect static files, expose port 8000, run with gunicorn
  - [ ] 10.2.2 — Create `docker-compose.yml`: single service for the Django app, volume for SQLite database, environment variables from `.env` file
  - [ ] 10.2.3 — Create `.dockerignore`: exclude `.git`, `__pycache__`, `*.pyc`, `.env`, `db.sqlite3`, `node_modules`

- [ ] **10.3 — Static Files & Production Settings**
  - [ ] 10.3.1 — Configure `STATIC_ROOT` and run `collectstatic`
  - [ ] 10.3.2 — Add `whitenoise` middleware for serving static files in production
  - [ ] 10.3.3 — Set `DEBUG = False` handling, configure `ALLOWED_HOSTS` from environment

- [ ] **10.4 — Documentation**
  - [ ] 10.4.1 — Create `README.md` with: project description, features list, tech stack, setup instructions (local and Docker), environment variables reference, and screenshots placeholder
  - [ ] 10.4.2 — Add inline code comments to complex views and services
  - [ ] 10.4.3 — Create `CHANGELOG.md` with version 1.0 release notes