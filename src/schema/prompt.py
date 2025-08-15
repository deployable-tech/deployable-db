from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from ..base import Base

class PromptTemplate(Base):
    __tablename__ = "prompts"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    content = Column(JSON, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)