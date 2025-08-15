from sqlalchemy.orm import Session
import uuid
from ..schema.user import User, WebSession

def create_user(db: Session, email: str, hashed_password: str) -> User:
    user = User(id=str(uuid.uuid4()), email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: str, **kwargs) -> User:
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def update_web_session(db: Session, session_id: str, **kwargs) -> WebSession:
    sess = get_web_session(db, session_id)
    if not sess:
        return None
    for key, value in kwargs.items():
        setattr(sess, key, value)
    db.commit()
    db.refresh(sess)
    return sess
