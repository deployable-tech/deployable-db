from sqlalchemy.orm import Session
from ..schema.prompt import PromptTemplate

def create_prompt(db: Session, prompt_id: str, name: str, content: dict) -> PromptTemplate:
    prompt = PromptTemplate(id=prompt_id, name=name, content=content)
    db.add(prompt)
    db.commit()
    return prompt

def get_prompt(db: Session, prompt_id: str):
    return db.query(PromptTemplate).filter(PromptTemplate.id == prompt_id).first()

def list_prompts(db: Session):
    return db.query(PromptTemplate).all()

def update_prompt(db: Session, prompt_id: str, **kwargs) -> PromptTemplate:
    prompt = get_prompt(db, prompt_id)
    if not prompt:
        return None
    for key, value in kwargs.items():
        setattr(prompt, key, value)
    db.commit()
    db.refresh(prompt)
    return prompt

def delete_prompt(db: Session, prompt_id: str) -> bool:
    prompt = get_prompt(db, prompt_id)
    if not prompt:
        return False
    db.delete(prompt)
    db.commit()
    return True
