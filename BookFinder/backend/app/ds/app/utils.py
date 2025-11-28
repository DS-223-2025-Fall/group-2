"""
Utility functions for data loading, processing, and helpers
"""
import pandas as pd
import csv
from pathlib import Path
from typing import List, Dict, Optional


def load_books_from_csv(file_path: str, encoding: str = 'utf-8') -> List[Dict]:
    """
    Load books from CSV file
    
    Args:
        file_path: Path to CSV file
        encoding: File encoding
        
    Returns:
        List of book dictionaries
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        books = df.to_dict('records')
        print(f"Loaded {len(books)} books from {file_path}")
        return books
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []


def filter_books_with_descriptions(books: List[Dict], description_field: str = 'description') -> List[Dict]:
    """
    Filter books that have non-empty descriptions
    
    Args:
        books: List of book dictionaries
        description_field: Name of description field
        
    Returns:
        Filtered list of books
    """
    filtered = [
        book for book in books 
        if description_field in book and 
        book[description_field] and 
        str(book[description_field]).strip() and
        str(book[description_field]).strip().lower() != 'nan'
    ]
    print(f"Filtered {len(filtered)} books with descriptions out of {len(books)}")
    return filtered






def format_recommendation_output(recommendations: List[Dict]) -> str:
    """
    Format recommendations as readable text
    
    Args:
        recommendations: List of recommendation dictionaries
        
    Returns:
        Formatted string
    """
    if not recommendations:
        return "No recommendations found."
    
    output = []
    output.append("\n" + "="*70)
    output.append("RECOMMENDATIONS")
    output.append("="*70 + "\n")
    
    for rec in recommendations:
        output.append(f"#{rec['rank']} - {rec['title']}")
        output.append(f"    Author: {rec.get('author', 'Unknown')}")
        output.append(f"    Book ID: {rec['book_id']}")
        output.append(f"    Similarity: {rec['similarity_percentage']}%")
        output.append("")
    
    return "\n".join(output)


def validate_book_data(books: List[Dict], required_fields: List[str] = None) -> bool:
    """
    Validate that book data has required fields
    
    Args:
        books: List of book dictionaries
        required_fields: List of required field names
        
    Returns:
        True if valid, False otherwise
    """
    if not books:
        print("Error: No books provided")
        return False
    
    required_fields = required_fields or ['book_id', 'title', 'description']
    
    for i, book in enumerate(books[:10]):  # Check first 10
        for field in required_fields:
            if field not in book:
                print(f"Error: Book {i} missing required field '{field}'")
                return False
    
    print(f"Validation passed for {len(books)} books")
    return True


def get_book_by_id(books: List[Dict], book_id: str) -> Optional[Dict]:
    """
    Find a book by its ID
    
    Args:
        books: List of book dictionaries
        book_id: Book ID to search for
        
    Returns:
        Book dictionary if found, None otherwise
    """
    for book in books:
        if book.get('book_id') == book_id or book.get('ISBN') == book_id:
            return book
    return None


def calculate_cosine_similarity(vec1, vec2) -> float:
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score
    """
    import numpy as np
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def batch_process(items: List, batch_size: int = 100):
    """
    Generator to process items in batches
    
    Args:
        items: List of items to process
        batch_size: Size of each batch
        
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def print_store_summary(store_stats: Dict):
    """
    Print a formatted summary of store statistics
    
    Args:
        store_stats: Store statistics dictionary
    """
    print("\n" + "="*60)
    print("VECTOR STORE SUMMARY")
    print("="*60)
    print(f"Store ID:        {store_stats.get('store_id')}")
    print(f"Model:           {store_stats.get('model')}")
    print(f"Embedding Dim:   {store_stats.get('embedding_dim')}")
    print(f"Total Vectors:   {store_stats.get('total_vectors')}")
    print(f"Index Exists:    {store_stats.get('index_exists')}")
    print(f"Metadata Exists: {store_stats.get('metadata_exists')}")
    print("="*60 + "\n")
