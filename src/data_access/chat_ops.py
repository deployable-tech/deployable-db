from sqlalchemy.orm import Session
from typing import Iterable, List
from ..schema.chat import ChatSession, ChatExchange

def create_chat_session(db: Session, user_id: str) -> ChatSession:
    sess = ChatSession(user_id=user_id)
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

def get_chat_session(db: Session, session_id: str):
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()

def add_chat_exchange(
    db: Session,
    session_id: str,
    user_message: str,
    rag_prompt: str,
    assistant_message: str,
    html_response: str,
    context_used: Iterable[dict],
) -> ChatExchange:
    exchange = ChatExchange(
        session_id=session_id,
        user_message=user_message,
        rag_prompt=rag_prompt,
        assistant_message=assistant_message,
        html_response=html_response,
        context_used=list(context_used),
    )
    db.add(exchange)
    db.commit()
    db.refresh(exchange)
    return exchange

def list_chat_sessions(db: Session, user_id: str) -> List[ChatSession]:
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()

def update_chat_session(db: Session, session_id: str, **kwargs) -> ChatSession:
    sess = get_chat_session(db, session_id)
    if not sess:
        return None
    for key, value in kwargs.items():
        setattr(sess, key, value)
    db.commit()
    db.refresh(sess)
    return sess

def delete_chat_session(db: Session, session_id: str) -> bool:
    sess = get_chat_session(db, session_id)
    if not sess:
        return False
    db.delete(sess)
    db.commit()
    return True

def get_chat_exchange(db: Session, exchange_id: int) -> ChatExchange:
    return db.query(ChatExchange).filter(ChatExchange.id == exchange_id).first()

def list_chat_exchanges(db: Session, session_id: str) -> List[ChatExchange]:
    return db.query(ChatExchange).filter(ChatExchange.session_id == session_id).all()

def update_chat_exchange(db: Session, exchange_id: int, **kwargs) -> ChatExchange:
    exch = get_chat_exchange(db, exchange_id)
    if not exch:
        return None
    for key, value in kwargs.items():
        setattr(exch, key, value)
    db.commit()
    db.refresh(exch)
    return exch

def delete_chat_exchange(db: Session, exchange_id: int) -> bool:
    exch = get_chat_exchange(db, exchange_id)
    if not exch:
        return False
    db.delete(exch)
    db.commit()
    return True
