from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from ..base import Base
import uuid

def _uuid() -> str:
    return str(uuid.uuid4())

class Document(Base):
    __tablename__ = "documents"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True, default=_uuid)
    filename: str = Column(String, nullable=False)
    stored_filename: str = Column(String, nullable=False)  # renamed storage name
    path: str = Column(String, nullable=False)
    tags = Column(JSON, default=list)
    uploaded_at: datetime = Column(DateTime, default=datetime.utcnow)