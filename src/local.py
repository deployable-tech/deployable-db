"""Utilities for working with a local SQLite database.

This module provides a small helper that lets the rest of the application
operate against a SQLite file on disk.  It mirrors the ``db_session``
context manager from :mod:`__init__` but allows callers to specify a
file path, making it trivial to spin up a self‑contained database for
development or testing.

Example
-------
>>> from db import repository
>>> from db.local import local_session
>>> with local_session("/tmp/example.db") as session:
...     repository.create_user(session, "user@example.com", "hashed")

The SQLite file will be created on demand if it does not already exist.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from sqlalchemy.orm import sessionmaker

from . import Base, _create_engine, _default_sqlite_path


@contextmanager
def local_session(db_path: str | Path | None = None):
    """Yield a session bound to a SQLite database on the local filesystem.

    Parameters
    ----------
    db_path:
        Optional path to the SQLite database file.  If omitted, a
        platform‑appropriate default location is chosen (the same logic
        used by the main package when no ``DATABASE_URL`` is supplied).

    The session commits on successful exit and rolls back if an
    exception occurs.
    """

    sqlite_path = Path(db_path) if db_path else _default_sqlite_path()
    url = f"sqlite:///{sqlite_path.as_posix()}"
    engine = _create_engine(url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Ensure tables exist before handing out the session.
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()

