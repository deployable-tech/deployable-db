"""CRUD operations for LLM services and models."""
from __future__ import annotations

import uuid
from typing import List

from sqlalchemy.orm import Session

from ..schema.llm import LLMService, LLMModel


def create_service(
    db: Session,
    name: str,
    provider: str,
    base_url: str | None = None,
    auth_ref: str | None = None,
    timeout_sec: int | None = None,
    extra: dict | None = None,
) -> LLMService:
    """Create and persist a new LLM service."""
    svc = LLMService(
        id=str(uuid.uuid4()),
        name=name,
        provider=provider,
        base_url=base_url,
        auth_ref=auth_ref,
        timeout_sec=timeout_sec,
        extra=extra or {},
    )
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


def list_services(db: Session) -> List[LLMService]:
    """Return all LLM services."""
    return db.query(LLMService).all()


def get_service(db: Session, service_id: str) -> LLMService | None:
    """Fetch a service by its ID."""
    return db.query(LLMService).filter(LLMService.id == service_id).first()


def update_service(db: Session, service_id: str, **kwargs) -> LLMService | None:
    """Update fields on an existing service."""
    svc = get_service(db, service_id)
    if not svc:
        return None
    for key, value in kwargs.items():
        setattr(svc, key, value)
    db.commit()
    db.refresh(svc)
    return svc


def create_model(
    db: Session,
    service_id: str,
    name: str,
    modality: str | None = None,
    context_window: int | None = None,
    supports_tools: bool = False,
    extra: dict | None = None,
) -> LLMModel:
    """Create and persist a new LLM model under a service."""
    model = LLMModel(
        id=str(uuid.uuid4()),
        service_id=service_id,
        name=name,
        modality=modality,
        context_window=context_window,
        supports_tools=supports_tools,
        extra=extra or {},
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def list_models(db: Session, service_id: str | None = None) -> List[LLMModel]:
    """List models, optionally filtered by service."""
    query = db.query(LLMModel)
    if service_id:
        query = query.filter(LLMModel.service_id == service_id)
    return query.all()


def get_model(db: Session, model_id: str) -> LLMModel | None:
    """Fetch a model by its ID."""
    return db.query(LLMModel).filter(LLMModel.id == model_id).first()


def update_model(db: Session, model_id: str, **kwargs) -> LLMModel | None:
    """Update fields on an existing model."""
    model = get_model(db, model_id)
    if not model:
        return None
    for key, value in kwargs.items():
        setattr(model, key, value)
    db.commit()
    db.refresh(model)
    return model
