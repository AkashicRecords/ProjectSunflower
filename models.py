from sqlalchemy import Column, Integer, String, Text
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    subject = Column(String, index=True)