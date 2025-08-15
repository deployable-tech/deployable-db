import os
import platform
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

APP_NAME = os.getenv("APP_NAME", "deployable-knowledge")

def _default_sqlite_path() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        data_dir = base / APP_NAME
    elif system == "Darwin":
        data_dir = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        data_dir = base / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "app.db"

def _resolve_db_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url and url.strip():
        return url
    sqlite_path = _default_sqlite_path()
    return f"sqlite:///{sqlite_path.as_posix()}"

DATABASE_URL = _resolve_db_url()

def _create_engine(url: str):
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    engine = create_engine(url, pool_pre_ping=True, connect_args=connect_args)
    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _sqlite_pragmas(dbapi_conn, _):
            cur = dbapi_conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON;")
            cur.execute("PRAGMA journal_mode=WAL;")
            cur.execute("PRAGMA synchronous=NORMAL;")
            cur.close()
    return engine

engine = _create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
