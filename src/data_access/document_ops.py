from sqlalchemy.orm import Session
from typing import Iterable
from ..schema.document import Document

def create_document(
    db: Session,
    *,
    filename: str,
    path: str,
    tags: Iterable[str] | None = None,
) -> Document:
    doc = Document(filename=filename, path=path, tags=list(tags or []))
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: str):
    return db.query(Document).filter(Document.id == doc_id).first()

def list_documents(db: Session):
    return db.query(Document).all()

from ..utils.file_store import store_local_file

def create_document_with_file(
    db: Session,
    *,
    src_path: str,
    original_filename: str,
    storage_dir: str,
    tags: Iterable[str] | None = None,
) -> Document:
    """Store file locally and create a document record."""
    stored_filename, stored_path = store_local_file(src_path, storage_dir)
    doc = Document(
        filename=original_filename,
        stored_filename=stored_filename,
        path=stored_path,
        tags=list(tags or [])
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
import os

def update_document(db: Session, doc_id: str, **kwargs) -> Document:
    doc = get_document(db, doc_id)
    if not doc:
        return None
    for key, value in kwargs.items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

def delete_document(db: Session, doc_id: str, delete_file: bool = True) -> bool:
    doc = get_document(db, doc_id)
    if not doc:
        return False
    if delete_file and doc.path and os.path.exists(doc.path):
        try:
            os.remove(doc.path)
        except OSError:
            pass
    db.delete(doc)
    db.commit()
    return True
