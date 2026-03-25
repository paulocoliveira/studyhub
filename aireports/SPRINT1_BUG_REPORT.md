# Sprint 1 — Bug Report
## StudyHub — Project Setup & Authentication

**Date:** 2026-03-25
**Environment:** Django 6.0.3 · Python 3.13 · SQLite
**Identified by:** QA automated (Django Test Client) + static analysis
**Total bugs:** 2
**Fixed:** 1 (during QA)
**Pending:** 1 (Sprint 7)

---

## Index

| ID | Severity | Component | Status |
|----|----------|-----------|--------|
| [B-01](#b-01) | Low | `users/tests.py` | Pending — Sprint 7 |
| [B-02](#b-02) | Medium | `core/settings.py` | Fixed |

---

## B-01

**Title:** `users/tests.py` is empty — no automated unit tests

**Severity:** Low
**Component:** `users/tests.py`
**Status:** Pending — Sprint 7
**Discovered in:** TC-16
**Fix date:** Sprint 7

### Description

The `users/tests.py` file shipped from `python manage.py startapp` contains only the default comment. Running `python manage.py test users` reports 0 tests ran. There is no regression coverage for registration, login, logout, `EmailBackend`, or `CustomUserManager`.

### Steps to reproduce

```bash
source .venv/bin/activate
python manage.py test users --verbosity=2
# Output: Ran 0 tests in 0.000s — OK (no test cases)
```

### Expected behavior

At minimum, tests covering: user creation via `CustomUserManager`, email-based login via `EmailBackend`, registration with duplicate email rejected, login with wrong password rejected.

### Actual behavior

```
Ran 0 tests in 0.000s
OK
```

### Root cause

`users/tests.py` was never populated. Sprint 1 focused on implementation; Sprint 7 is planned for the testing pass.

### Fix

Write unit tests in `users/tests.py` as part of Sprint 7 (tasks 7.1.1, 7.1.2, 7.1.3).

### Impact

Without automated tests, any future refactor of the auth flow can silently break registration or login. Risk is low in early sprint but grows as complexity increases.

---

## B-02

**Title:** `ALLOWED_HOSTS = []` rejects test client requests and fails in non-debug deployments

**Severity:** Medium
**Component:** `core/settings.py`
**Status:** Fixed
**Discovered in:** Static analysis during TC-16
**Fix date:** 2026-03-25

### Description

`ALLOWED_HOSTS` was set to an empty list `[]`. While Django's dev server in `DEBUG=True` mode implicitly allows `localhost` and `127.0.0.1`, the Django test client sends requests with `HTTP_HOST: testserver`, which is blocked by `SecurityMiddleware` when `ALLOWED_HOSTS` is empty. Additionally, any staging or production deployment where `DEBUG=False` would fail immediately for all hosts.

### Steps to reproduce

```python
# With ALLOWED_HOSTS = [] and DEBUG = False
from django.test import Client
c = Client()
response = c.get('/')
# Raises SuspiciousOperation: Invalid HTTP_HOST header: 'testserver'
# Results in HTTP 400 Bad Request
```

### Expected behavior

`ALLOWED_HOSTS` should include at minimum `'127.0.0.1'`, `'localhost'`, and `'testserver'` for development and testing.

### Actual behavior

```python
ALLOWED_HOSTS = []  # blocks test client and all production hosts
```

### Root cause

The default Django project scaffold leaves `ALLOWED_HOSTS = []`, relying on developers to populate it. The initial settings configuration task (1.1.2) did not include adding development hosts.

### Fix applied

**File:** `core/settings.py`

```python
# Before
ALLOWED_HOSTS = []

# After
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
```

### Impact

Without this fix, running automated tests (`python manage.py test`) against any URL resolving through the test client would fail with HTTP 400 once `DEBUG=False`. Affected: all 14 automated test cases in TC-02 through TC-14. In practice, tests passed in the QA session because the test client bypasses some host checks in debug mode, but the underlying misconfiguration would cause failures in any CI/CD pipeline.

---

## Fix Summary

| ID | Modified file | Change | Migration needed |
|----|--------------|--------|-----------------|
| B-01 | `users/tests.py` | Write unit tests (Sprint 7) | No |
| B-02 | `core/settings.py` | Added `'127.0.0.1'`, `'localhost'`, `'testserver'` to `ALLOWED_HOSTS` | No |
