from pydantic import BaseModel
from typing import Optional

class BookInfoGet(BaseModel):
    search_query: str

class BookInfo(BaseModel):
    bookId: str
    bookName: str
    isbn: str
    title: str
    author: str
    genre: str
    description: str
    language: str
    data_source: str
    
class BookStoreInfo(BaseModel):
    storeId: str
    storeName: str
    address: str
    city: str
    phone: str
    website_url: str
    email: str
    latitude: float
    longitude: float
    price: float = 0.0  # Price of book at this store
    
class FullBookInfo(BookInfo):
    stores: list[BookStoreInfo]
    book: BookInfo
    match_type: Optional[str] = None  # "exact", "fuzzy", "semantic", "external", or None
    is_recommendation: bool = False  # True if this is a recommendation, False if main result