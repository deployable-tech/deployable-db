from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
import uuid

def _uuid() -> str:
    return str(uuid.uuid4())

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True, default=_uuid)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    summary: str = Column(Text, default="")
    title: str = Column(String, default="")
    persona: str | None = Column(String, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    exchanges: List["ChatExchange"] = relationship(
        "ChatExchange", back_populates="session", cascade="all, delete-orphan"
    )

class ChatExchange(Base):
    __tablename__ = "chat_exchanges"
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    session_id: str = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    user_message: str = Column(Text)
    rag_prompt: str = Column(Text)
    assistant_message: str = Column(Text)
    html_response: str = Column(Text)
    context_used = Column(JSON, default=list)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="exchanges")