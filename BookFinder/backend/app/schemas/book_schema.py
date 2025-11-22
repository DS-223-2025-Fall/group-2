from pydantic import BaseModel

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
    
class FullBookInfo(BookInfo):
    stores: list[BookStoreInfo]
    book: BookInfo