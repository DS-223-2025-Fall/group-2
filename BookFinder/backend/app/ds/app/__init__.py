"""
DS Service - Book Recommendation System
Semantic search for book recommendations using embeddings
"""

# Initialize logging first
from .logging_config import init_default_logging
init_default_logging()

from .book_recommender import BookRecommendationService, find_similar_books
from .vector_store import VectorStore
from .description_generator import DescriptionGenerator
from .config import config

__all__ = [
    'BookRecommendationService',
    'find_similar_books',
    'VectorStore',
    'DescriptionGenerator',
    'config'
]
