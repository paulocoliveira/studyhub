---
name: Sprint 1 Foundation — Auth & Project Scaffold
description: Records key architectural decisions made during Sprint 1 backend setup that are not obvious from the code alone
type: project
---

The dashboard app was deleted from git at some point and had to be manually recreated (directory + __init__.py, apps.py, models.py, admin.py, tests.py, migrations/__init__.py). It owns no models — that is intentional.

The original db.sqlite3 was seeded with admin migrations based on Django's default User model. When AUTH_USER_MODEL was changed to users.CustomUser, the DB became inconsistent and had to be deleted and re-migrated from scratch. This is expected Django behavior when changing AUTH_USER_MODEL on an existing DB.

**Why:** AUTH_USER_MODEL must be set before the first migrate; changing it after is painful. The project is now correctly bootstrapped.

**How to apply:** Never change AUTH_USER_MODEL after migrations have been applied without also resetting the DB or writing a careful data migration. In this project, the DB was reset cleanly at Sprint 1.
