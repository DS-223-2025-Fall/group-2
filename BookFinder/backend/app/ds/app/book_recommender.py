"""
Book Recommendation Service
Orchestrates the full pipeline: generate description -> embed -> search -> return top-k books
"""
import logging
from typing import List, Tuple, Optional
import time

try:
    from .description_generator import DescriptionGenerator
    from .vector_store import VectorStore
    from .config import config
except ImportError:
    from description_generator import DescriptionGenerator
    from vector_store import VectorStore
    from config import config

logger = logging.getLogger(__name__)


class BookRecommendationService:
    """
    **Service for book recommendations.**
    
    Handles the complete flow from query to recommendations.
    """
    
    def __init__(self):
        """**Initialize** the recommendation service."""
        logger.info("="*70)
        logger.info("Initializing BookRecommendationService...")
        logger.info("="*70)
        
        self.description_generator = DescriptionGenerator()
        self.vector_store = VectorStore()
        
        logger.info("="*70)
        logger.info("✓ Service initialized successfully")
        logger.info("="*70)
    
    def find_similar_books(
        self,
        query_title: str,
        top_k: Optional[int] = None
    ) -> List[dict]:
        """
        **Find books similar to the query title.**
        
        Args:
            query_title: Title of the book user is searching for
            top_k: Number of recommendations to return (default from config)
            
        Returns:
            List of book recommendations with similarity scores
        """
        top_k = top_k or config.TOP_K_RESULTS
        
        print(f"\n{'='*70}")
        print(f"[BookRecommendationService] FINDING SIMILAR BOOKS")
        print(f"{'='*70}")
        print(f"Query Title: '{query_title}'")
        print(f"Top-K: {top_k}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Step 1: Generate description for the query title
        print(f"{'─'*70}")
        print("STEP 1: Generate Book Description")
        print(f"{'─'*70}")
        query_description = self.description_generator.generate_description(query_title)
        
        # Step 2: Load vector store if not already loaded
        print(f"{'─'*70}")
        print("STEP 2: Load Vector Store")
        print(f"{'─'*70}")
        
        if not self.vector_store.load_index():
            raise ValueError(f"Vector store not found. Please build the index first.")
        
        # Step 3: Search for similar books
        print(f"{'─'*70}")
        print("STEP 3: Search for Similar Books")
        print(f"{'─'*70}")
        results = self.vector_store.search(query_description, top_k=top_k)
        
        # Step 4: Format results
        print(f"{'─'*70}")
        print("STEP 4: Format Results")
        print(f"{'─'*70}")
        recommendations = []
        for idx, (metadata, similarity) in enumerate(results, 1):
            rec = {
                "rank": idx,
                "book_id": metadata.get("book_id"),
                "similarity_score": round(similarity, 4),
                "similarity_percentage": round(similarity * 100, 2)
            }
            recommendations.append(rec)
            print(f"  #{idx}: ISBN {rec['book_id']} - {rec['similarity_percentage']}%")
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print(f"[BookRecommendationService] ✓ COMPLETE")
        print(f"{'='*70}")
        print(f"Found {len(recommendations)} recommendations in {elapsed_time:.2f}s")
        print(f"{'='*70}\n")
        
        return recommendations
    
    def build_index(
        self,
        books_data: List[dict],
        description_field: str = "description"
    ):
        """
        **Build vector index from book data.**
        
        Args:
            books_data: List of book dictionaries with descriptions
            description_field: Name of the field containing descriptions
        """
        logger.info("="*70)
        logger.info(f"BUILDING INDEX")
        logger.info("="*70)
        logger.info(f"Total books: {len(books_data)}")
        logger.info("="*70)
        
        # Extract descriptions and metadata
        logger.info("Extracting descriptions and metadata...")
        descriptions = []
        metadata = []
        books_without_description = 0
        
        for book in books_data:
            # Get description or generate a fallback
            description = book.get(description_field, "").strip()
            
            # If no description, create a basic one from title and author
            if not description:
                books_without_description += 1
                title = book.get("title", "Unknown Title")
                author = book.get("author", "Unknown Author")
                genre = book.get("genre", "")
                
                # Fallback description
                description = f"{title} by {author}."
                if genre:
                    description += f" Genre: {genre}."
                
                logger.debug(f"No description for '{title}', using fallback")
            
            descriptions.append(description)
            metadata.append({
                "book_id": book.get("book_id") or book.get("ISBN")
            })
        
        if books_without_description > 0:
            logger.warning(f"{books_without_description} books had no description, using fallback text")
        
        logger.info(f"✓ Extracted {len(descriptions)} books for indexing")
        
        # Create and save the index
        self.vector_store.create_index(descriptions, metadata)
        self.vector_store.save_index()
        
        logger.info("="*70)
        logger.info(f"✓ Index built successfully")
        logger.info("="*70)
    
    def build_index_from_csv(self, csv_path: str, bookid_col: str = 'bookid', descr_col: str = 'descr'):
        """
        **Build vector index directly from a CSV file.**
        
        Args:
            csv_path: Path to CSV file
            bookid_col: Name of the book ID column
            descr_col: Name of the description column
        """
        logger.info("="*70)
        logger.info("BUILDING INDEX FROM CSV")
        logger.info("="*70)
        logger.info(f"CSV Path: {csv_path}")
        logger.info(f"Book ID column: {bookid_col}")
        logger.info(f"Description column: {descr_col}")
        logger.info("="*70)
        
        self.vector_store.load_from_csv(csv_path, bookid_col, descr_col)
        
        logger.info("="*70)
        logger.info(f"✓ Index built successfully from CSV")
        logger.info("="*70)
    
    def build_index_from_database(
        self,
        store_id: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        **Deprecated:** Build vector index from database. Use CSV instead."""   
        raise NotImplementedError("Database loading removed. Please use build_index_from_csv() instead.")
    
    def add_books(
        self,
        new_books: List[dict],
        description_field: str = "description"
    ):
        """
        **Add new books to the existing vector index.**
        
        Args:
            new_books: List of new book dictionaries
            description_field: Name of the field containing descriptions
        """
        if not self.vector_store.load_index():
            raise ValueError(f"Vector store not found. Build it first.")
        
        # Extract descriptions and metadata (only ISBN)
        descriptions = []
        metadata = []
        
        for book in new_books:
            if description_field in book and book[description_field]:
                descriptions.append(book[description_field])
                metadata.append({
                    "book_id": book.get("book_id") or book.get("ISBN")
                })
        
        self.vector_store.add_books(descriptions, metadata)
        self.vector_store.save_index()
        
        print(f"Added {len(descriptions)} books to index")
    
    def get_stats(self) -> dict:
        """**Get statistics for the vector store.**"""
        return self.vector_store.get_stats()
    
    def delete_index(self):
        """**Delete the vector index.**"""
        self.vector_store.delete_index()
    
    def get_cache_stats(self) -> dict:
        """**Get description cache statistics.**"""
        return self.description_generator.get_cache_stats()


# Convenience function for quick usage
def find_similar_books(query_title: str, top_k: int = 5) -> List[dict]:
    """
    **Convenience function to find similar books quickly.**
    
    Args:
        query_title: Title to search for
        top_k: Number of results
        
    Returns:
        List of recommendations
    """
    service = BookRecommendationService()
    return service.find_similar_books(query_title, top_k)
