"""Simple demonstration script for the db package.

Creates a user in a temporary SQLite database using the local_session
helper and verifies that the repository interface works.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))
import src as db
sys.modules["db"] = db


import tempfile
from db.local import local_session
from db import repository


def main() -> None:
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        with local_session(tmp.name) as session:
            user = repository.create_user(session, "demo@example.com", "hashed")
            fetched = repository.get_user(session, user.id)
            assert fetched is not None and fetched.email == "demo@example.com"
            print(f"User {fetched.email} created and fetched successfully")


if __name__ == "__main__":
    main()
