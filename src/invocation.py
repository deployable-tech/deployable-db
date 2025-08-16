"""Universal invocation payload for LLM calls."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class InvocationParams:
    """Generic parameters for invoking an LLM model via any provider."""

    service_id: str
    model_name: str
    messages: List[Dict[str, Any]] = field(default_factory=list)
    prompt: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    tools: List[Dict[str, Any]] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)
