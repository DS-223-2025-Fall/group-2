from typing import List
from schemas.book_schema import BookStoreInfo, FullBookInfo, BookInfo

from typing import List
from schemas.book_schema import FullBookInfo, BookInfo, BookStoreInfo

import psycopg2

# Temporary untill DB is fully ready
def get_allBooks() -> List[FullBookInfo]:
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


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()

# -------------------------------------------------------
# BOOK METHODS
# -------------------------------------------------------

def get_book_by_id(book_id):

    cur.execute("""
        SELECT * FROM book WHERE book_id = %s
    """, (book_id,))

    result = cur.fetchone()
    conn.close()
    return result


def search_books_by_title(search_term):
    cur.execute("""
        SELECT * FROM book
        WHERE LOWER(title) LIKE LOWER(%s)
        LIMIT 20
    """, (f"%{search_term}%",))

    results = cur.fetchall()
    conn.close()
    return results


def insert_book(title, author, genre, description, isbn, source="local"):


    cur.execute("""
        INSERT INTO book (title, author, genre, description, isbn, data_source)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING book_id
    """, (title, author, genre, description, isbn, source))

    book_id = cur.fetchone()["book_id"]
    conn.commit()
    conn.close()
    return book_id


# -------------------------------------------------------
# BOOKSTORE + INVENTORY METHODS
# -------------------------------------------------------

def get_stores_for_book(book_id):

    cur.execute("""
        SELECT bs.store_name, bs.address, bsi.price
        FROM book_store_inventory bsi
        JOIN bookstore bs ON bsi.store_id = bs.store_id
        WHERE bsi.book_id = %s
        ORDER BY bsi.price ASC
    """, (book_id,))

    results = cur.fetchall()
    conn.close()
    return results


def insert_inventory_entry(book_id, store_id, price):

    cur.execute("""
        INSERT INTO book_store_inventory (book_id, store_id, price)
        VALUES (%s, %s, %s)
        ON CONFLICT (book_id, store_id)
        DO UPDATE SET price = EXCLUDED.price;
    """, (book_id, store_id, price))

    conn.commit()
    conn.close()


# -------------------------------------------------------
# SIMILARITY METHODS
# -------------------------------------------------------

def get_similar_books(book_id, top_n=10):

    cur.execute("""
        SELECT b2.*, bs.similarity_score
        FROM book_similarity bs
        JOIN book b2 ON b2.book_id = bs.book_id_2
        WHERE bs.book_id_1 = %s
        ORDER BY bs.similarity_score DESC
        LIMIT %s
    """, (book_id, top_n))

    results = cur.fetchall()
    conn.close()
    return results


def insert_similarity(book1, book2, score):

    cur.execute("""
        INSERT INTO book_similarity (book_id_1, book_id_2, similarity_score)
        VALUES (%s, %s, %s)
        ON CONFLICT (book_id_1, book_id_2)
        DO UPDATE SET similarity_score = EXCLUDED.similarity_score;
    """, (book1, book2, score))

    conn.commit()
    conn.close()


# -------------------------------------------------------
# SEARCH LOGGING METHODS
# -------------------------------------------------------

def log_search_query(term, matched_book_id=None):

    cur.execute("""
        INSERT INTO search_query (search_term, matched_book_id)
        VALUES (%s, %s)
    """, (term, matched_book_id))

    conn.commit()
    conn.close()


def get_recent_searches(limit=20):

    cur.execute("""
        SELECT * FROM search_query
        ORDER BY query_id DESC
        LIMIT %s
    """, (limit,))

    results = cur.fetchall()
    conn.close()
    return results


# -------------------------------------------------------
# HEALTH CHECK (useful for backend readiness)
# -------------------------------------------------------

def health_check():
    try:
        conn.close()
        return True
    except:
        return False