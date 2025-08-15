"""Simple demonstration script for the db package.

Creates a user in a temporary SQLite database using the local_session
helper and verifies that the data_access interface works.
"""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile

# Add src folder to sys.path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

# Import the refactored db package
import src as db
sys.modules["db"] = db

# Import from new locations
from db.utils.local import local_session
from db.data_access import user_ops


def main() -> None:
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        with local_session(tmp.name) as session:
            user = user_ops.create_user(session, "demo@example.com", "hashed")
            fetched = user_ops.get_user(session, user.id)
            assert fetched is not None and fetched.email == "demo@example.com"
            print(f"User {fetched.email} created and fetched successfully")


if __name__ == "__main__":
    main()
