# Deployable DB Reference

This package provides a lightweight interface to the application's
persistent data using [SQLAlchemy](https://www.sqlalchemy.org/).  It can
target any database supported by SQLAlchemy but defaults to a local
SQLite file when no `DATABASE_URL` environment variable is defined.

## Initialising the database

```python
from db import init_db

# Create tables if they do not already exist
init_db()
```

## Obtaining a session

For general usage the package exposes a `db_session` context manager
which yields a short‑lived SQLAlchemy `Session`:

```python
from db import db_session, repository

with db_session() as session:
    user = repository.create_user(session, "user@example.com", "hashed")
```

## Using a local SQLite file

During development or testing it is often convenient to work with a
self‑contained SQLite database stored on the local filesystem.  The
`local_session` helper makes this easy:

```python
from db.local import local_session
from db import repository

with local_session("/tmp/example.db") as session:
    repository.create_user(session, "user@example.com", "hashed")
```

If no path is supplied, a platform‑appropriate default location is used.

## Repository helpers

The `repository` module contains simple CRUD helpers for the core ORM
models (`User`, `ChatSession`, `PromptTemplate`, etc.).  These functions
expect an active SQLAlchemy `Session` and can be used with either the
default engine or a session created via `local_session`.

## Environment variables

`DATABASE_URL` – optional database connection string.  When unset the
package falls back to a persistent SQLite file under the user's data
directory.

`APP_NAME` – overrides the default application directory used when the
package creates a SQLite file automatically.

