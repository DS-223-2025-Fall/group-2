import json

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

output_path = "books.jsonl"

with open(output_path, "w", encoding="utf-8") as f:
    for title, description in books.items():
        line = json.dumps({title: description}, ensure_ascii=False)
        f.write(line + "\n")

print("books.jsonl created!")
