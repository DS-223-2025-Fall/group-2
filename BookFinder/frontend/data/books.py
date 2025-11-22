"""
Mock book data for FindMyRead application.
In production, this would be replaced with API calls to the backend.
"""

BOOKS = [
    {
        "id": 1,
        "title": "Anna Karenina",
        "author": "Leo Tolstoy",
        "description": "A tragic love story set in 19th century Russia.",
        "long_description": "Anna Karenina is a profound exploration of love, marriage, and societal expectations in 19th-century Russia. Tolstoy weaves multiple narratives that examine the moral complexities of human relationships, social mores, and the struggle between personal fulfillment and duty. The novel's sweeping scope and unforgettable characters make it a timeless classic.",
        "rating": 4.9,
        "store": {"name": "Bookinist", "price": 9500, "currency": "AMD"},
    },
    {
        "id": 2,
        "title": "The Name of the Rose",
        "author": "Umberto Eco",
        "description": "A medieval mystery set in an Italian monastery.",
        "long_description": "The Name of the Rose is a historical mystery set in 14th-century Italy, following Brother William of Baskerville as he investigates a series of murders at a Benedictine abbey. Eco overlays a richly researched medieval setting with philosophical debates, semiotics, and intricate plotting. This edition explores the tension between reason and faith through a dense, atmospheric narrative.",
        "rating": 4.5,
        "store": {"name": "Zangak", "price": 8500, "currency": "AMD"},
    },
    {
        "id": 3,
        "title": "The Name of the Rose (Epigraph Edition)",
        "author": "Umberto Eco",
        "description": "A medieval mystery set in an Italian monastery.",
        "long_description": "This special epigraph edition includes additional annotations and insights into Eco's layering of historical detail, literary allusion, and medieval scholarship. The story remains a tightly crafted mystery with philosophical undertones, enriched here by extra content and scholarly notes.",
        "rating": 4.5,
        "store": {"name": "Epigraph", "price": 9200, "currency": "AMD"},
    },
]

BOOKSTORES = ["Zangak", "Epigraph", "Books.am", "Nor Graxanut", "Phoenix", "Bookinist"]
