from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
import uuid

def _uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True, default=_uuid)
    email: str = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    llm_config = Column(JSON, default=dict)

    sessions: List["WebSession"] = relationship("WebSession", back_populates="user")
    chat_sessions: List["ChatSession"] = relationship(
        "ChatSession", back_populates="user", cascade="all, delete-orphan"
    )

class WebSession(Base):
    __tablename__ = "web_sessions"
    __allow_unmapped__ = True

    session_id: str = Column(String, primary_key=True)
    user_id: str = Column(String, ForeignKey("users.id"), nullable=False)
    issued_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: datetime = Column(DateTime, nullable=False)
    last_seen: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    ua_hash: str | None = Column(String, nullable=True)
    ip_net: str | None = Column(String, nullable=True)
    attrs = Column(JSON, default=dict)

    user = relationship("User", back_populates="sessions")