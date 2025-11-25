from loguru import logger

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    DECIMAL,
    Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime

from db.postgres import Base, engine

# ==========================================
# USER TABLE
# ==========================================
class AppUser(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)

    ratings = relationship("Ratings", back_populates="user")
    queries = relationship("SearchQuery", back_populates="user")


# ==========================================
# BOOK TABLE
# ==========================================
class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True)
    ISBN = Column(String(50), unique=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    genre = Column(String(100))
    description = Column(Text)
    language = Column(String(50))
    data_source = Column(String(100))
    url = Column(String(255))

    inventory = relationship("BookStoreInventory", back_populates="book")
    similarities_1 = relationship(
        "BookSimilarity",
        foreign_keys="BookSimilarity.book_id_1",
        back_populates="book1"
    )
    similarities_2 = relationship(
        "BookSimilarity",
        foreign_keys="BookSimilarity.book_id_2",
        back_populates="book2"
    )


# ==========================================
# BOOKSTORE TABLE
# ==========================================
class Bookstore(Base):
    __tablename__ = "bookstore"

    store_id = Column(Integer, primary_key=True)
    store_name = Column(String(255), nullable=False)
    address = Column(String(255))
    city = Column(String(100))
    phone = Column(String(50))
    website_url = Column(String(255))
    email = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

    inventory = relationship("BookStoreInventory", back_populates="store")


# ==========================================
# BOOK_STORE_INVENTORY TABLE
# ==========================================
class BookStoreInventory(Base):
    __tablename__ = "book_store_inventory"
    __table_args__ = (
        UniqueConstraint("book_id", "store_id", name="idx_inventory_unique"),
    )

    inventory_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey("bookstore.store_id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(10, 2))

    book = relationship("Book", back_populates="inventory")
    store = relationship("Bookstore", back_populates="inventory")


# ==========================================
# BOOK_SIMILARITY TABLE
# ==========================================
class BookSimilarity(Base):
    __tablename__ = "book_similarity"
    __table_args__ = (
        UniqueConstraint("book_id_1", "book_id_2", name="idx_unique_similarity"),
    )

    similarity_id = Column(Integer, primary_key=True)
    book_id_1 = Column(Integer, ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    book_id_2 = Column(Integer, ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    similarity_score = Column(Float)

    book1 = relationship("Book", foreign_keys=[book_id_1], back_populates="similarities_1")
    book2 = relationship("Book", foreign_keys=[book_id_2], back_populates="similarities_2")


# ==========================================
# SEARCH_QUERY TABLE
# ==========================================
class SearchQuery(Base):
    __tablename__ = "search_query"

    query_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("app_user.user_id"))
    search_term = Column(String(255), nullable=False)
    matched_book_id = Column(Integer, ForeignKey("book.book_id"))

    user = relationship("AppUser", back_populates="queries")
    matched_book = relationship("Book")


# ==========================================
# RATINGS TABLE
# ==========================================
class Ratings(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("app_user.user_id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)

    user = relationship("AppUser", back_populates="ratings")
    book = relationship("Book")
    
    
