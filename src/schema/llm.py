"""Schema definitions for LLM services and models."""
from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from ..base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class LLMService(Base):
    """Represents an LLM endpoint/service configuration."""

    __tablename__ = "llm_services"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True, default=_uuid)
    name: str = Column(String, unique=True, nullable=False)
    provider: str = Column(String, nullable=False)
    base_url: str | None = Column(String, nullable=True)
    auth_ref: str | None = Column(String, nullable=True)
    timeout_sec: int | None = Column(Integer, nullable=True)
    is_enabled: bool = Column(Boolean, default=True, nullable=False)
    extra = Column(JSON, default=dict)

    models: List["LLMModel"] = relationship(
        "LLMModel", back_populates="service", cascade="all, delete-orphan"
    )


class LLMModel(Base):
    """Represents a model available under a given service."""

    __tablename__ = "llm_models"
    __allow_unmapped__ = True

    id: str = Column(String, primary_key=True, default=_uuid)
    service_id: str = Column(String, ForeignKey("llm_services.id"), nullable=False)
    name: str = Column(String, nullable=False)
    modality: str | None = Column(String, nullable=True)
    context_window: int | None = Column(Integer, nullable=True)
    supports_tools: bool = Column(Boolean, default=False, nullable=False)
    extra = Column(JSON, default=dict)

    service = relationship("LLMService", back_populates="models")
