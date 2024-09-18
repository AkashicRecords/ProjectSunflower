from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
import models, schemas

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chat).offset(skip).limit(limit).all()

def create_chat(db: Session, chat: schemas.ChatCreate):
    db_chat = models.Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def search_chats(db: Session, query: str, start_date: datetime = None, end_date: datetime = None):
    filters = [
        or_(
            models.Chat.title.ilike(f"%{query}%"),
            models.Chat.content.ilike(f"%{query}%"),
            models.Category.name.ilike(f"%{query}%")
        )
    ]
    
    if start_date:
        filters.append(models.Chat.timestamp >= start_date)
    if end_date:
        filters.append(models.Chat.timestamp <= end_date)
    
    return db.query(models.Chat).filter(
        and_(*filters)
    ).join(models.Category).all()

def update_chat(db: Session, chat_id: int, chat_update: schemas.ChatUpdate):
    db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if db_chat:
        update_data = chat_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_chat, key, value)
        db.commit()
        db.refresh(db_chat)
    return db_chat

def create_trigger_word(db: Session, trigger_word: schemas.TriggerWordCreate):
    db_trigger_word = models.TriggerWord(**trigger_word.dict())
    db.add(db_trigger_word)
    db.commit()
    db.refresh(db_trigger_word)
    return db_trigger_word

def get_trigger_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TriggerWord).offset(skip).limit(limit).all()

def get_trigger_words_by_category(db: Session, category_id: int):
    return db.query(models.TriggerWord).filter(models.TriggerWord.category_id == category_id).all()

def delete_trigger_word(db: Session, trigger_word_id: int):
    db_trigger_word = db.query(models.TriggerWord).filter(models.TriggerWord.id == trigger_word_id).first()
    if db_trigger_word:
        db.delete(db_trigger_word)
        db.commit()
        return True
    return False