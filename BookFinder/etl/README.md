# 📚 Entity-Relationship Diagram (ERD) Description

This ERD models a database schema for a system that appears to manage **Books**, **Bookstores**, **User Search Queries**, and **Ratings**.

---

## 🏛️ Entities and Attributes

The diagram contains the following main entities:

### 1. **USER**
Represents an individual user of the system.
* **user\_id** (int): Primary Key (PK).
* **email** (string): Unique Key (UK), likely used for login/identification.

### 2. **SEARCH\_QUERY**
Records the search activities performed by users.
* **query\_id** (int): Primary Key (PK).
* **user\_id** (int): Foreign Key (FK) referencing **USER**.
* **search\_term** (string): The actual text the user searched for.
* **matched\_isbn** (string): Foreign Key (FK) referencing **BOOK**, indicating which book, if any, the search successfully matched.

### 3. **BOOK**
Details about a specific book.
* **isbn** (string): Primary Key (PK). (International Standard Book Number)
* **title** (string): The book's title.
* **author** (string): The book's author.
* **genre** (string): The book's category or genre.
* **description** (text): A long-form description of the book.
* **language** (string): The language the book is written in.

### 4. **BOOKSTORE**
Details about a physical bookstore.
* **store\_id** (int): Primary Key (PK).
* **store\_name** (string): The name of the store.
* **address** (string): The street address.
* **city** (string): The city where the store is located.
* **phone** (string): The store's phone number.
* **website\_url** (string): The store's official website.
* **email** (string): The store's email address.
* **latitude** (float): Geographic latitude coordinate.
* **longitude** (float): Geographic longitude coordinate.

### 5. **BOOK\_STORE\_INVENTORY**
A junction entity that models the many-to-many relationship between **BOOKSTORE** and **BOOK**, representing the stock of books in each store.
* **inventory\_id** (int): Primary Key (PK).
* **isbn** (string): Foreign Key (FK) referencing **BOOK**.
* **store\_id** (int): Foreign Key (FK) referencing **BOOKSTORE**.
* **price** (decimal): The price of the book at that specific store.

### 6. **RATINGS**
Records the ratings and comments users provide for books.
* **rating\_id** (int): Primary Key (PK).
* **user\_id** (int): Foreign Key (FK) referencing **USER**.
* **isbn** (string): Foreign Key (FK) referencing **BOOK**.
* **rating** (int): The numerical rating given (e.g., 1-5 stars).
* **comment** (string): Any associated text comment.

---

## 🔗 Relationships

The relationships describe how the entities interact with each other:

| Relationship | Entities Involved | Type | Description |
| :--- | :--- | :--- | :--- |
| **performs** | **USER** and **SEARCH\_QUERY** | 1:M (One-to-Many) | A **USER** *performs* one or more **SEARCH\_QUERY** records. |
| **refers** | **USER** and **RATINGS** | 1:M (One-to-Many) | A **USER** *raises* one or more **RATINGS** for different books. |
| **references** | **SEARCH\_QUERY** and **BOOK** | M:1 (Many-to-One) | A **SEARCH\_QUERY** *references* zero or one **BOOK** (via `matched_isbn`). |
| **rated\_on** | **RATINGS** and **BOOK** | M:1 (Many-to-One) | **RATINGS** are *rated\_on* one specific **BOOK**. |
| **stocks** | **BOOKSTORE** and **BOOK\_STORE\_INVENTORY** | 1:M (One-to-Many) | A **BOOKSTORE** *stocks* many items in its **BOOK\_STORE\_INVENTORY**. |
| **stocked\_in** | **BOOK** and **BOOK\_STORE\_INVENTORY** | 1:M (One-to-Many) | A **BOOK** is *stocked\_in* multiple entries in the **BOOK\_STORE\_INVENTORY** (one for each store that stocks it). |

---

## 🔑 Key Constraints

* **Primary Keys (PK):** Uniquely identify each record (e.g., `user_id`, `isbn`, `store_id`).
* **Foreign Keys (FK):** Enforce referential integrity by linking tables (e.g., `user_id` in `SEARCH_QUERY` links to `USER`).
* **Unique Key (UK):** Ensures all values in the column are unique (e.g., `email` in `USER`).
* **The combination of `isbn` and `store_id` in `BOOK_STORE_INVENTORY` likely forms a Composite Unique Key** to ensure a price is only listed once for a specific book at a specific store (though not explicitly shown as a PK, this is a common design pattern for inventory).