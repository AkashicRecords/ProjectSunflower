from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    chats = relationship("Chat", back_populates="category")
    trigger_words = relationship("TriggerWord", back_populates="category")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="chats")

class TriggerWord(Base):
    __tablename__ = "trigger_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="trigger_words")