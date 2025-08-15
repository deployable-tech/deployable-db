"""
Database engine/session setup and initialization.
"""

from .base import Base
from .base import engine, SessionLocal
from .schema import *

def init_db() -> None:
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
