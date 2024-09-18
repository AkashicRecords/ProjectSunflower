from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    trigger_words: List[TriggerWord] = []

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    timestamp: datetime
    category: Optional[Category] = None

    class Config:
        orm_mode = True

class ChatImport(BaseModel):
    chats: List[ChatCreate]

class TriggerWordBase(BaseModel):
    word: str
    category_id: int

class TriggerWordCreate(TriggerWordBase):
    pass

class TriggerWord(TriggerWordBase):
    id: int

    class Config:
        orm_mode = True

class ConversationExport(BaseModel):
    title: str
    content: str