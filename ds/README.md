# 📚 Semantic Book Search (SentenceTransformer)

A small Python project that allows to search for classic books **by title or by meaning** using SentenceTransformer embeddings.  
Users can type a book name or a theme (e.g., “dystopian future”) and the model finds the closest match semantically.

---

# 🏗️ Project Structure

```
project/
│
├── books.py               # Main semantic search application
├── books_jsonl.py         # Script that generates books.jsonl
├── books.jsonl            # Data file (generated automatically)
├── requirements.txt       # Python dependencies (optional)
└── README.md              # Documentation
```

### **File Descriptions**

| File             | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `books.py`       | Loads SentenceTransformer, reads the JSONL books, performs title-based and meaning-based search. |
| `books_jsonl.py` | Generates the `books.jsonl` dataset from a Python dictionary. Run once to create/update the file. |
| `books.jsonl`    | JSONL dataset containing book title → description pairs. Auto-generated. |
| `requirements.txt` | Optional list of dependencies. |

---

# 📄 Data Format (`books.jsonl`)

Each line contains a single key-value pair:

```
{"The Great Gatsby": "A tragic love story set in the 1920s..."}
{"1984": "Dystopian masterpiece about a totalitarian regime..."}
{"Pride and Prejudice": "Witty romance between Elizabeth Bennet and Mr. Darcy..."}
```

This format is required by `books.py`.

---

# ▶️ How to Run the Project

## 1️⃣ Install Dependencies


```bash
python -m venv venv
```

```bash
venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Generate the Dataset

Run this **once**:

```bash
python books_jsonl.py
```

Output:

```
books.jsonl created!
```

---

## 3️⃣ Run the Book Search Program

```bash
python books.py
```

Startup output:

```
Loading AI model... (only once)
Loading book data from books.jsonl...
Preparing book database...
Ready! You can now search by title or meaning.
```

---

# 💡 Example Usage

### **Example 1 — Semantic Search**

**User Input:**
```
Enter book title or theme: dystopian future
```

**Program Output:**
```
Searching for books similar to: "dystopian future"
BEST MATCH:
Title: 1984
Similarity: 84.2%
Dystopian masterpiece about a totalitarian regime, constant surveillance...
```

---

### **Example 2 — Exact Title Match**

**User Input:**
```
Enter book title or theme: The Hobbit
```

**Program Output:**
```
FOUND IT!
Title: The Hobbit
Bilbo Baggins, a hobbit, joins dwarves and wizard Gandalf...
```




