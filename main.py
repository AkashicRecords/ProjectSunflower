from fastapi import FastAPI, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import re

import crud, models, schemas
from database import SessionLocal, engine

# Set up OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")

def create_tables():
    models.Base.metadata.create_all(bind=engine)

create_tables()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/import-chats/", response_model=List[schemas.Chat])
def import_chats(chats_import: schemas.ChatImport, db: Session = Depends(get_db)):
    imported_chats = []
    for chat in chats_import.chats:
        category = categorize_chat(chat.content, db)
        chat.category_id = category.id
        imported_chat = crud.create_chat(db=db, chat=chat)
        imported_chats.append(imported_chat)
    return imported_chats

@app.get("/chats/", response_model=List[schemas.Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chats = crud.get_chats(db, skip=skip, limit=limit)
    return chats

@app.get("/chats/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@app.get("/search/")
def search_chats(
    query: str, 
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.search_chats(db, query, start_date, end_date)

def categorize_chat(content: str, db: Session) -> schemas.Category:
    # Check for the new topic phrase
    new_topic_match = re.search(r"Let's start a new topic called\s*(.+)", content)
    if new_topic_match:
        new_topic = new_topic_match.group(1).strip()
        # Create a new category
        new_category = crud.create_category(db, schemas.CategoryCreate(name=new_topic))
        return new_category

    # Check for the existing topic phrase
    existing_topic_match = re.search(r"Let's talk about\s*(.+)", content)
    if existing_topic_match:
        topic = existing_topic_match.group(1).strip()
        # Check if the category already exists
        existing_category = crud.get_category_by_name(db, topic)
        if existing_category:
            return existing_category
        else:
            # Create a new category if it doesn't exist
            new_category = crud.create_category(db, schemas.CategoryCreate(name=topic))
            return new_category

    # If no specific phrase is found, proceed with the existing categorization logic
    categories = crud.get_categories(db)
    category_scores = {category.id: 0 for category in categories}

    for category in categories:
        trigger_words = crud.get_trigger_words_by_category(db, category.id)
        category_scores[category.id] = sum(word.word.lower() in content.lower() for word in trigger_words)

    if all(score == 0 for score in category_scores.values()):
        # If no category matches, create or get a default "Uncategorized" category
        uncategorized = crud.get_category_by_name(db, "Uncategorized")
        if not uncategorized:
            uncategorized = crud.create_category(db, schemas.CategoryCreate(name="Uncategorized"))
        return uncategorized

    selected_category_id = max(category_scores, key=category_scores.get)
    return crud.get_category(db, selected_category_id)

@app.post("/trigger-words/", response_model=schemas.TriggerWord)
def create_trigger_word(trigger_word: schemas.TriggerWordCreate, db: Session = Depends(get_db)):
    return crud.create_trigger_word(db=db, trigger_word=trigger_word)

@app.get("/trigger-words/", response_model=List[schemas.TriggerWord])
def read_trigger_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trigger_words = crud.get_trigger_words(db, skip=skip, limit=limit)
    return trigger_words

@app.delete("/trigger-words/{trigger_word_id}")
def delete_trigger_word(trigger_word_id: int, db: Session = Depends(get_db)):
    success = crud.delete_trigger_word(db, trigger_word_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trigger word not found")
    return {"message": "Trigger word deleted successfully"}

@app.post("/intercept-chat/", response_model=schemas.Chat)
async def intercept_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    category = categorize_chat(chat.content, db)
    chat.category_id = category.id
    return crud.create_chat(db=db, chat=chat)

@app.post("/export-conversation/", response_model=schemas.Chat)
async def export_conversation(conversation: schemas.ConversationExport, db: Session = Depends(get_db)):
    # Categorize the entire conversation
    category = categorize_chat(conversation.content, db)
    
    # Create a new chat entry
    chat = schemas.ChatCreate(
        title=conversation.title,
        content=conversation.content,
        category_id=category.id
    )
    
    return crud.create_chat(db=db, chat=chat)