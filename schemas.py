from pydantic import BaseModel

class ChatBase(BaseModel):
    title: str
    content: str
    subject: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int

    class Config:
        orm_mode = True