from contextlib import contextmanager
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from ..base import Base, _create_engine, _default_sqlite_path

@contextmanager
def local_session(db_path: str | Path | None = None):
    sqlite_path = Path(db_path) if db_path else _default_sqlite_path()
    url = f"sqlite:///{sqlite_path.as_posix()}"
    engine = _create_engine(url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()
