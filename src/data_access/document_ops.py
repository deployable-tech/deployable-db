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
