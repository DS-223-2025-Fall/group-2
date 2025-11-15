from schemas.book_schema import BookInfo, BookStoreInfo, FullBookInfo

def get_books_service(search_query) -> list[FullBookInfo]:
    store1 = BookStoreInfo(
        storeId="s1",
        storeName="City Books",
        address="123 Main St",
        city="Yerevan",
        phone="+37491123456",
        website_url="http://citybooks.example.com",
        email="info@citybooks.example.com",
        latitude=40.1792,
        longitude=44.4991
    )

    store2 = BookStoreInfo(
        storeId="s2",
        storeName="Book World",
        address="456 Market Ave",
        city="Yerevan",
        phone="+37491234567",
        website_url="http://bookworld.example.com",
        email="contact@bookworld.example.com",
        latitude=40.1800,
        longitude=44.5000
    )

    book1 = BookInfo(
        bookId="b1",
        bookName="Harry Potter and the Philosopher's Stone",
        isbn="9780747532699",
        title="Harry Potter 1",
        author="J.K. Rowling",
        genre="Fantasy",
        description="A young wizard's journey begins.",
        language="English",
        data_source="dummy_data"
    )

    book2 = BookInfo(
        bookId="b2",
        bookName="The Lord of the Rings",
        isbn="9780618640157",
        title="LOTR",
        author="J.R.R. Tolkien",
        genre="Fantasy",
        description="Epic adventure in Middle-earth.",
        language="English",
        data_source="dummy_data"
    )

    full_book1 = FullBookInfo(
        book=book1,
        stores=[store1, store2],
        **book1.model_dump()
    )

    full_book2 = FullBookInfo(
        book=book2,
        stores=[store2],
        **book2.model_dump()
    )

    return [full_book1, full_book2]