# Backend API - Book Store

This is the backend API for managing books and ratings, built with **FastAPI**. It includes endpoints for retrieving books, adding ratings (protected), and fetching ratings. The backend also supports Google OAuth2 login.

---

## **Project Structure**

```
backend/
 ├── app/
 │    ├── main.py
 │    ├── routers/
 │    │    ├── books.py
 │    │    ├── ratings.py
 │    │    └── auth.py
 │    ├── schemas/
 │    └── services/
 ├── requirements.txt
 ├── Dockerfile
 └── .env
```

---

## **Environment Variables**

The backend reads configuration from `.env` or environment variables: This is for the oauth2 flow using Google.

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
API_SECRET_KEY=your-jwt-secret
```
---

## **Endpoints**

### **Books**

* **GET /books**
  Retrieve list of books (dummy data).

**Request Params (JSON):**

```json
{
  "search_query": "Harry Potter"
}
```

**Response (200 OK):**

```json
[
  {
    "bookId": "b1",
    "bookName": "Book One",
    "isbn": "123456",
    "title": "Book One Title",
    "author": "Author 1",
    "genre": "Fiction",
    "description": "A great book",
    "language": "English",
    "data_source": "dummy",
    "stores": [
      {
        "storeId": "s1",
        "storeName": "Store One",
        "address": "123 Street",
        "city": "Yerevan",
        "phone": "111-1111",
        "website_url": "https://store1.com",
        "email": "contact@store1.com",
        "latitude": 40.18,
        "longitude": 44.51
      }
    ]
  }
]
```

---

### **2️Ratings**

* **GET /ratings/{book_id}**  (Public)
  Get all ratings for a book.

**Example:**

```bash
GET /ratings/b1
```

**Response:**

```json
[
  {"bookId":"b1","user_email":"alice@example.com","rating":5, "comment": "Good book"},
  {"bookId":"b1","user_email":"bob@example.com","rating":4, "comment": "Good book"}
]
```

* **POST /ratings**  (Protected, requires JWT)
  Add or update a rating for a book.

**Request Body:**

```json
{
  "bookId": "b1",
  "rating": 5,
  "comment": "Good Book"
}
```

**Headers:**

```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**

```json
{"bookId":"b1","user_email":"newuser@example.com","rating":5,"comment": "Good book"}
```

---

### **3️⃣ Google OAuth2 Login**

* **GET /auth/google** → Starts Google OAuth2 login
* **GET /auth/google/callback** → Handles callback and returns JWT token

**Example response:**

```json
{
  "access_token": "YOUR_JWT_TOKEN",
  "token_type": "bearer",
  "user": {"email": "newuser@example.com", "name": "New User"}
}
```

---

## **Running with Docker**

### Firstly rename .env.example to .env.

### **1️⃣ Build Docker image**

From `backend/` folder:

```bash
docker build -t backend-api .
```

### **2️⃣ Run container**

```bash
docker run -d -p 8000:8000 backend-api
```

* API is now available at `http://localhost:8000`
* `/books` and `/ratings` endpoints can be tested

---

## **Notes**

* Filling `.env` is not needed yet, posting a rating will be available in the next milestone
