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
