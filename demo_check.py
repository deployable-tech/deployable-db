"""Comprehensive demonstration script for the db package.

Tests all major schema types and stores a sample document file locally.
Database is stored in ./local_db/demo.db
Documents are stored in ./documents/
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add src folder to sys.path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

# Import the refactored db package
import src as db
sys.modules["db"] = db

# Imports from new locations
from db.utils.local import local_session
from db.data_access import (
    user_ops,
    chat_ops,
    prompt_ops,
    document_ops
)

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    db_dir = base_dir / "local_db"
    docs_dir = base_dir / "documents"

    db_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)

    db_path = db_dir / "demo.db"

    with local_session(db_path) as session:
        # 1. Create a user
        user = user_ops.create_user(session, "demo@example.com", "hashed")
        print(f"Created user: {user.email}")

        # 2. Create a chat session for that user
        chat_session = chat_ops.create_chat_session(session, user.id)
        print(f"Created chat session: {chat_session.id}")

        # 3. Add a chat exchange
        exchange = chat_ops.add_chat_exchange(
            session,
            chat_session.id,
            user_message="Hello!",
            rag_prompt="Greeting intent detected",
            assistant_message="Hi there! How can I help?",
            html_response="<p>Hi there! How can I help?</p>",
            context_used=[{"note": "test context"}],
        )
        print(f"Added chat exchange: {exchange.id}")

        # 4. Create a prompt template
        prompt = prompt_ops.create_prompt(
            session,
            prompt_id="demo_prompt",
            name="Demo Prompt",
            content={"template": "Hello, {name}!"}
        )
        print(f"Created prompt: {prompt.name}")

        # 5. Create a dummy text file and store it as a document
        temp_file_path = docs_dir / "temp_source.txt"
        temp_file_path.write_text("This is a test document file.")

        doc = document_ops.create_document_with_file(
            session,
            src_path=temp_file_path,
            original_filename="example.txt",
            storage_dir=docs_dir,
            tags=["demo", "test"]
        )
        print(f"Stored document: {doc.filename} -> {doc.stored_filename}")

    print(f"\nDatabase saved to: {db_path}")
    print(f"Documents stored in: {docs_dir}")

if __name__ == "__main__":
    main()
