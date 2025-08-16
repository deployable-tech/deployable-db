# Deployable DB – Developer Reference

This package provides a clean, modular SQLAlchemy ORM layer for managing application data.

## 📂 Package Structure

```
db/
  __init__.py         # Engine/session setup, init_db()
  base.py             # DeclarativeBase and engine/session creation
  schema/             # Database table definitions
    user.py           # User + WebSession
    chat.py           # ChatSession + ChatExchange
    prompt.py         # PromptTemplate
    document.py       # Document metadata
  data_access/        # CRUD helpers for each schema
    user_ops.py
    chat_ops.py
    prompt_ops.py
    document_ops.py
  utils/
    local.py          # Local SQLite session helper
    file_store.py     # Local file renaming & storage for Documents
```

---

## ⚙️ Core Concepts

- **`schema/`** – Defines the database tables and their relationships.
- **`data_access/`** – High-level functions for Create, Read, Update, and Delete (CRUD) operations.
- **`utils/`** – Helper utilities for local database sessions and file handling.

---

## 🚀 Getting Started

```python
from db import init_db
init_db()  # Creates tables if they don't exist
```

Or, for testing / isolated databases:

```python
from db.utils.local import local_session

with local_session("mytest.db") as session:
    # Use data_access functions here
```

---

## 🧩 Entities & CRUD Functions

### 1. **User**
**Schema:** `schema/user.py` (`User`)

**CRUD:**
```python
from db.data_access import user_ops

user = user_ops.create_user(session, "user@example.com", "hashed_pw")
fetched = user_ops.get_user(session, user.id)
user_ops.update_user(session, user.id, email="new@example.com")
user_ops.delete_user(session, user.id)
```

---

### 2. **WebSession**
**Schema:** `schema/user.py` (`WebSession`)

**CRUD:**
```python
from datetime import datetime, timedelta
from db.data_access import user_ops

sess = user_ops.create_web_session(
    session,
    session_id="abc123",
    user_id=user.id,
    issued_at=datetime.utcnow(),
    expires_at=datetime.utcnow() + timedelta(days=1)
)
fetched = user_ops.get_web_session(session, "abc123")
user_ops.update_web_session(session, "abc123", ip_net="192.168.0.0/24")
user_ops.delete_web_session(session, "abc123")
```

---

### 3. **ChatSession**
**Schema:** `schema/chat.py` (`ChatSession`)

**CRUD:**
```python
from db.data_access import chat_ops

chat_sess = chat_ops.create_chat_session(session, user.id)
fetched = chat_ops.get_chat_session(session, chat_sess.id)
chat_ops.update_chat_session(session, chat_sess.id, title="New Title")
chat_ops.delete_chat_session(session, chat_sess.id)
```

---

### 4. **ChatExchange**
**Schema:** `schema/chat.py` (`ChatExchange`)

**CRUD:**
```python
exch = chat_ops.add_chat_exchange(
    session,
    chat_sess.id,
    user_message="Hello",
    rag_prompt="Prompt",
    assistant_message="Hi!",
    html_response="<p>Hi!</p>",
    context_used=[{"info": "test"}]
)
fetched = chat_ops.get_chat_exchange(session, exch.id)
all_exchanges = chat_ops.list_chat_exchanges(session, chat_sess.id)
chat_ops.update_chat_exchange(session, exch.id, assistant_message="Updated message")
chat_ops.delete_chat_exchange(session, exch.id)
```

---

### 5. **PromptTemplate**
**Schema:** `schema/prompt.py` (`PromptTemplate`)

**CRUD:**
```python
from db.data_access import prompt_ops

prompt = prompt_ops.create_prompt(session, "p1", "Greeting", {"text": "Hello {name}"})
fetched = prompt_ops.get_prompt(session, "p1")
prompt_ops.update_prompt(session, "p1", name="New Greeting")
prompt_ops.delete_prompt(session, "p1")
```

---

### 6. **Document**
**Schema:** `schema/document.py` (`Document`)

**CRUD:**
```python
from db.data_access import document_ops

# Create directly
doc = document_ops.create_document(
    session,
    filename="original.txt",
    path="/path/to/original.txt",
    tags=["tag1"]
)

# Or create with file storage (recommended)
from pathlib import Path
tmp_file = Path("temp.txt")
tmp_file.write_text("Hello world")

doc = document_ops.create_document_with_file(
    session,
    src_path=tmp_file,
    original_filename="original.txt",
    storage_dir="documents",  # Will be created if missing
    tags=["tag1"]
)

fetched = document_ops.get_document(session, doc.id)
document_ops.update_document(session, doc.id, tags=["updated"])
document_ops.delete_document(session, doc.id, delete_file=True)
```

**Special Notes:**
- `create_document_with_file()` renames the file to a UUID + extension in `storage_dir` and saves its original name in `filename`.
- `delete_document(..., delete_file=True)` removes both the DB entry and the file from disk.

---

### 7. **LLMService & LLMModel**
**Schema:** `schema/llm.py` (`LLMService`, `LLMModel`)

**CRUD:**
```python
from db.data_access import llm_ops

svc = llm_ops.create_service(session, "openai-prod", "openai", base_url="https://api.openai.com/v1", auth_ref="openai_key")
model = llm_ops.create_model(session, svc.id, "gpt-4o", modality="chat", supports_tools=True)
services = llm_ops.list_services(session)

from db.invocation import InvocationParams
payload = InvocationParams(
    service_id=svc.id,
    model_name="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.5,
)
```

---
## 📌 Utility Reference

### `local_session(db_path=None)`
- Creates a temporary or persistent SQLite DB session.
- Commits on success, rolls back on exception.

### `store_local_file(src_path, storage_dir)`
- Moves a file to a storage directory, renaming it to a UUID.
- Returns `(stored_filename, final_path)`.

---

## ✅ Best Practices

- Always interact with DB tables via the `data_access` layer, not the ORM classes directly.
- For documents, prefer `create_document_with_file()` to ensure safe, unique file storage.
- Use `local_session()` for testing, and `init_db()` for production startup.
