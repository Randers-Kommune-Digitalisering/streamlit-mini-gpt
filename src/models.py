from sqlalchemy import Column, Integer, String, DateTime  # , Boolean, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'File'
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    assistant_id = Column(String, nullable=False)  # Changed from Integer to String
    azure_file_id = Column(String, nullable=False)  # New column for Azure file ID
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


# class Chat(Base):
#     __tablename__ = 'Chat'
#     chat_id = Column(Integer, primary_key=True, autoincrement=True)
#     assistant_id = Column(Integer, nullable=False)
#     user_id = Column(Integer, nullable=False)
#     timestamp = Column(DateTime, nullable=False)
