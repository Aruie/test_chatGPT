from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base, engine

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(50), index=True, unique = True , nullable=False)
    password = Column(String(256), nullable=False)

class Bot(Base):
    __tablename__ = "bots"
    bot_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(50), index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    memory = Column(Text)

class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True, index=True, nullable=False)
    bot_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

