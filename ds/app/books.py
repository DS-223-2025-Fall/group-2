from sentence_transformers import SentenceTransformer
import numpy as np
import json

# Load the SentenceTransformer model
print("Loading AI model... (only once)")
model = SentenceTransformer('all-MiniLM-L6-v2')

books = {
    "The Great Gatsby": "A tragic love story set in the 1920s about wealth, obsession, and the American Dream. Jay Gatsby throws lavish parties while chasing his lost love Daisy.",
    "1984": "Dystopian masterpiece about a totalitarian regime, constant surveillance, Big Brother, and the fight for truth and freedom.",
    "Pride and Prejudice": "Witty romance between Elizabeth Bennet and Mr. Darcy. Full of social class, misunderstandings, and personal growth.",
    "Brave New World": "Future society where humans are engineered, happiness is forced, and individuality is destroyed by technology and control.",
    "To Kill a Mockingbird": "Powerful story of racism, justice, and childhood innocence as Scout watches her father defend a Black man in the 1930s South.",
    "The Catcher in the Rye": "Teenager Holden Caulfield runs away and struggles with growing up, phoniness, and protecting childhood innocence.",
    "Animal Farm": "Satirical fable where farm animals revolt against humans, but pigs become the new tyrants. A warning about power and corruption.",
    "Wuthering Heights": "Dark gothic tale of passionate, destructive love between Heathcliff and Catherine across two generations on the wild moors.",
    "The Hobbit": "Bilbo Baggins, a hobbit, joins dwarves and wizard Gandalf on a fantasy quest to defeat dragon Smaug and reclaim treasure.",
    "The Hunger Games": "In a dystopian future, Katniss Everdeen fights to survive in a brutal televised death match controlled by a cruel government."
}

titles = list(books.keys())
descriptions = list(books.values())

# Pre-compute all embeddings
print("Preparing book database...")
embeddings = model.encode(titles, convert_to_numpy=True)
print("Ready! You can now search by title or meaning.\n")

list_of_books = ["The Great Gastby", "1984", "Pride Predujice", "Brave New World",]
# Main loop
for query in list_of_books:
    # query = input("Enter book title or theme (or 'quit' to exit): ").strip()

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
    print(f"\nSearching for books with name similar to: \"{query}\"")
    query_embedding = model.encode(query)
    similarities = np.dot(embeddings, query_embedding)
    best_idx = np.argmax(similarities)

    best_title = titles[best_idx]
    score = similarities[best_idx]

    print(f"BEST MATCH:")
    print(f"Title: {best_title}")
    print(f"Similarity: {score*100:.1f}%")
    print(f"{books[best_title]}\n")
