from loguru import logger


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from Database.database import Base, engine

# More tables will be added as we gather data for them

class Book(Base):
    __tablename__ = "book"

    isbn = Column(String, primary_key=True)
    title = Column(Text)
    author = Column(Text)
    genre = Column(Text)
    language = Column(Text)
    data_source = Column(Text)
    description = Column(Text)
    
Base.metadata.create_all(engine)