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
