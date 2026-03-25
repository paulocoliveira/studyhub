# Sprint 1 — Test Report
## StudyHub — Project Setup & Authentication

**Execution date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite · TailwindCSS CDN
**Method:** Django Test Client (automated script via `manage.py shell`) + static code analysis
**Executed by:** Claude Code (studyhub-qa-tester agent)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total tests | 16 |
| PASS | 15 |
| WARN | 1 |
| FAIL | 0 |
| Bugs found | 2 |
| Bugs fixed during sprint | 1 |
| Bugs pending (next sprint) | 1 |

**Overall result:** APPROVED WITH NOTES — no critical or blocking failures. The full authentication flow (landing page, registration, validation, login, logout, authenticated redirect) is functional.

---

## Test Scope

### Components tested

| Component | File | Status |
|-----------|------|--------|
| `CustomUser` model | `users/models.py` | Tested |
| `CustomUserManager` | `users/models.py` | Tested |
| `EmailBackend` | `users/backends.py` | Tested |
| `CustomUserCreationForm` | `users/forms.py` | Tested |
| `EmailAuthenticationForm` | `users/forms.py` | Tested |
| `RegisterView` | `users/views.py` | Tested |
| `CustomLoginView` | `users/views.py` | Tested |
| `CustomLogoutView` | `users/views.py` | Tested |
| `LandingPageView` | `core/views.py` | Tested |
| `DashboardView` | `dashboard/urls.py` | Tested |
| Template `register.html` | `templates/users/register.html` | Tested |
| Template `login.html` | `templates/users/login.html` | Tested |
| Template `landing.html` | `templates/landing.html` | Tested |
| Template `base.html` | `templates/base.html` | Tested |
| Template `base_public.html` | `templates/base_public.html` | Tested |
| URLs `users/urls.py` | `users/urls.py` | Tested |
| Root URL `/` | `core/urls.py` | Tested |
| `core/settings.py` configuration | `core/settings.py` | Tested |

### Components out of scope (Sprint 2+)

- Categories, Tags, Contents, Insights apps (stubs only)
- Dashboard full implementation (Sprint 4)
- Password reset flow
- `users/tests.py` automated test suite (Sprint 7)

---

## Test Cases

### TC-01 — Django system check

| Field | Value |
|-------|-------|
| **ID** | TC-01 |
| **Task** | 1.1 |
| **Description** | Verify `python manage.py check` reports no errors |
| **Command** | `python manage.py check` |
| **Expected result** | `System check identified no issues (0 silenced).` |
| **Actual result** | `System check identified no issues (0 silenced).` |
| **Status** | **PASS** |

---

### TC-02 — Landing page access (unauthenticated)

| Field | Value |
|-------|-------|
| **ID** | TC-02 |
| **Task** | 1.7 |
| **Description** | Verify `GET /` returns HTTP 200 with landing page rendered |
| **Input** | `GET /` (unauthenticated) |
| **Expected result** | HTTP 200 |
| **Actual result** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-03 — Registration page access

| Field | Value |
|-------|-------|
| **ID** | TC-03 |
| **Task** | 1.5, 1.6 |
| **Description** | Verify `GET /users/register/` renders registration form |
| **Input** | `GET /users/register/` |
| **Expected result** | HTTP 200 with form |
| **Actual result** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-04 — Login page access

| Field | Value |
|-------|-------|
| **ID** | TC-04 |
| **Task** | 1.5, 1.6 |
| **Description** | Verify `GET /users/login/` renders login form |
| **Input** | `GET /users/login/` |
| **Expected result** | HTTP 200 with form |
| **Actual result** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-05 — Registration with invalid email

| Field | Value |
|-------|-------|
| **ID** | TC-05 |
| **Task** | 1.5.1 |
| **Description** | Verify form rejects malformed email with error message |
| **Input** | `POST /users/register/` with `email=not-an-email` |
| **Expected result** | HTTP 200 + email validation error, no user created |
| **Actual result** | HTTP 200 + validation error, `CustomUser.objects.count()` unchanged |
| **Status** | **PASS** |

---

### TC-06 — Registration with weak password

| Field | Value |
|-------|-------|
| **ID** | TC-06 |
| **Task** | 1.5.1 |
| **Description** | Verify form rejects passwords that fail Django validators |
| **Input** | `POST /users/register/` with `password1=123`, `password2=123` |
| **Expected result** | HTTP 200 + password validation errors, no user created |
| **Actual result** | HTTP 200 + password errors, user count unchanged |
| **Status** | **PASS** |

---

### TC-07 — Registration with valid data

| Field | Value |
|-------|-------|
| **ID** | TC-07 |
| **Task** | 1.5.2 |
| **Description** | Verify valid registration creates a user in the database |
| **Input** | `POST /users/register/` with `email=test@studyhub.com`, `first_name=Test`, `last_name=User`, `password1=TestPass123!`, `password2=TestPass123!` |
| **Expected result** | User created in database |
| **Actual result** | `CustomUser.objects.get(email='test@studyhub.com')` succeeds |
| **Status** | **PASS** |

---

### TC-08 — Redirect after registration

| Field | Value |
|-------|-------|
| **ID** | TC-08 |
| **Task** | 1.5.2 |
| **Description** | Verify valid registration redirects to login page |
| **Expected result** | HTTP 302 to `/users/login/` |
| **Actual result** | HTTP 302 to `/users/login/` |
| **Status** | **PASS** |

---

### TC-09 — Login with invalid credentials

| Field | Value |
|-------|-------|
| **ID** | TC-09 |
| **Task** | 1.5.3 |
| **Description** | Verify login with wrong email/password shows error, no 500 |
| **Input** | `POST /users/login/` with `username=wrong@test.com`, `password=wrongpassword` |
| **Expected result** | HTTP 200 + error message visible |
| **Actual result** | HTTP 200 + error message rendered |
| **Status** | **PASS** |

---

### TC-10 — Login with valid credentials

| Field | Value |
|-------|-------|
| **ID** | TC-10 |
| **Task** | 1.5.3 |
| **Description** | Verify correct credentials authenticate and redirect to dashboard |
| **Input** | `POST /users/login/` with `username=test@studyhub.com`, `password=TestPass123!` |
| **Expected result** | HTTP 302 to `/dashboard/` |
| **Actual result** | HTTP 302 to `/dashboard/` |
| **Status** | **PASS** |

---

### TC-11 — Authenticated user accessing login page

| Field | Value |
|-------|-------|
| **ID** | TC-11 |
| **Task** | 1.5.3 |
| **Description** | Verify already-authenticated user is redirected away from login |
| **Pre-condition** | User authenticated in session |
| **Input** | `GET /users/login/` |
| **Expected result** | HTTP 302 to `/dashboard/` |
| **Actual result** | HTTP 302 to `/dashboard/` |
| **Status** | **PASS** |

---

### TC-12 — Logout

| Field | Value |
|-------|-------|
| **ID** | TC-12 |
| **Task** | 1.5.4 |
| **Description** | Verify `POST /users/logout/` ends session and redirects |
| **Pre-condition** | User authenticated |
| **Input** | `POST /users/logout/` |
| **Expected result** | HTTP 302 to `/` |
| **Actual result** | HTTP 302 to `/` |
| **Status** | **PASS** |

---

### TC-13 — Unauthenticated access to dashboard

| Field | Value |
|-------|-------|
| **ID** | TC-13 |
| **Task** | 1.5, 4.1 |
| **Description** | Verify unauthenticated user is redirected to login when accessing dashboard |
| **Input** | `GET /dashboard/` (no session) |
| **Expected result** | HTTP 302 to `/users/login/?next=/dashboard/` |
| **Actual result** | HTTP 302 to `/users/login/?next=/dashboard/` |
| **Status** | **PASS** |

---

### TC-14 — Landing page authenticated redirect

| Field | Value |
|-------|-------|
| **ID** | TC-14 |
| **Task** | 1.7.1 |
| **Description** | Verify authenticated user accessing `/` is redirected to dashboard |
| **Pre-condition** | User authenticated |
| **Input** | `GET /` |
| **Expected result** | HTTP 302 to `/dashboard/` |
| **Actual result** | HTTP 302 to `/dashboard/` |
| **Status** | **PASS** |

---

### TC-15 — Static analysis: templates exist

| Field | Value |
|-------|-------|
| **ID** | TC-15 |
| **Task** | 1.3, 1.6, 1.7 |
| **Description** | Verify all required template files exist |
| **Checked** | `base.html`, `base_public.html`, `landing.html`, `users/register.html`, `users/login.html`, `users/password_change.html`, `components/sidebar.html`, `components/topbar.html`, `components/messages.html` |
| **Status** | **PASS** |

---

### TC-16 — User automated test suite

| Field | Value |
|-------|-------|
| **ID** | TC-16 |
| **Task** | Sprint 7 pre-check |
| **Description** | Verify `python manage.py test users` runs without errors |
| **Actual result** | 0 tests ran — `users/tests.py` is empty |
| **Bug associated** | B-01 |
| **Status** | **WARN — pending Sprint 7** |

---

## Bugs Found During Testing

| ID | Priority | Status | Description |
|----|----------|--------|-------------|
| B-01 | Low | Pending (Sprint 7) | `users/tests.py` is empty — no automated unit tests |
| B-02 | Medium | Fixed | `ALLOWED_HOSTS = []` breaks test client and production deployments |

> Full details in `SPRINT1_BUG_REPORT.md`

---

## Task Coverage

| Task | Description | Tested | Result |
|------|-------------|--------|--------|
| 1.1 | Initialize Django Project | Yes | PASS |
| 1.2 | Set up TailwindCSS | Yes (static analysis) | PASS |
| 1.3 | Create base templates | Yes | PASS |
| 1.4 | Custom user model | Yes | PASS |
| 1.5 | Authentication views | Yes | PASS |
| 1.6 | Authentication templates | Yes | PASS |
| 1.7 | Landing page | Yes | PASS |

---

## Test Environment

```
Operating system    : macOS Darwin 25.3.0
Python              : 3.13
Django              : 6.0.3
Database            : SQLite (db.sqlite3)
Authentication      : users.backends.EmailBackend
AUTH_USER_MODEL     : users.CustomUser
LOGIN_URL           : /users/login/
LOGIN_REDIRECT_URL  : /dashboard/
LOGOUT_REDIRECT_URL : /
```
