from typing import List
from schemas.book_schema import BookStoreInfo, FullBookInfo, BookInfo

from typing import List
from schemas.book_schema import FullBookInfo, BookInfo, BookStoreInfo

def get_allBooks() -> List[FullBookInfo]:
    books = []

    book = BookInfo(
        bookId="1",
        bookName="1984",
        isbn="1234567890",
        title="1984",
        author="George Orwell",
        genre="Dystopian",
        description="A dystopian novel...",
        language="en",
        data_source="internal"
    )

    stores = [
        BookStoreInfo(
            storeId="1",
            storeName="Awesome Books",
            address="123 Main St",
            city="NY",
            phone="123-456-7890",
            website_url="https://awesomebooks.com",
            email="info@awesomebooks.com",
            latitude=40.7128,
            longitude=-74.0060
        )
    ]

    full = FullBookInfo(
        **book.dict(),  # inherited fields
        book=book,      # REQUIRED
        stores=stores   # REQUIRED
    )

    return [full]
