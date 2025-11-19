from sentence_transformers import SentenceTransformer
import numpy as np
import json

# Load the SentenceTransformer model
print("Loading AI model... (only once)")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load books from .jsonl where each line is {"Title": "Description"}
books = {}
print("Loading book data from books.jsonl...")
with open("books.jsonl", "r") as f:
    for i, line in enumerate(f, start=1):
        try:
            entry = json.loads(line)
            if len(entry) == 1:
                title, description = list(entry.items())[0]
                books[title] = description
            else:
                print(f"⚠️ Line {i} skipped: Expected exactly one title-description pair.")
        except json.JSONDecodeError as e:
            print(f"❌ Line {i} is invalid JSON: {e}")

if not books:
    raise ValueError("❌ No valid book entries found. Please check your books.jsonl file.")

titles = list(books.keys())
descriptions = list(books.values())

# Pre-compute all embeddings
print("Preparing book database...")
embeddings = model.encode(descriptions, convert_to_numpy=True)
print("Ready! You can now search by title or meaning.\n")

# Main loop
while True:
    query = input("Enter book title or theme (or 'quit' to exit): ").strip()

    if query.lower() in ["quit", "exit", "q", ""]:
        print("\nThanks for using the Book Recommender! See you!")
        break

    # Try exact title match
    found = None
    for title in titles:
        if query.lower() in title.lower() or title.lower() in query.lower():
            found = title
            break

    if found:
        print(f"\nFOUND IT!")
        print(f"Title: {found}")
        print(f"{books[found]}\n")
        continue

    # Semantic search
    print(f"\nSearching for books similar to: \"{query}\"")
    query_embedding = model.encode(query)
    similarities = np.dot(embeddings, query_embedding)
    best_idx = np.argmax(similarities)

    best_title = titles[best_idx]
    score = similarities[best_idx]

    print(f"BEST MATCH:")
    print(f"Title: {best_title}")
    print(f"Similarity: {score*100:.1f}%")
    print(f"{books[best_title]}\n")
