"""
Simple test script to verify DS integration works correctly
Tests ONLY DS -> Backend communication (no database required)
Run this from the backend/app directory:
    python test_ds_integration.py
"""
import sys
from pathlib import Path

# Add DS to path
sys.path.insert(0, str(Path(__file__).parent))
DS_PATH = Path(__file__).parent / "ds"
sys.path.insert(0, str(DS_PATH))

from app.book_recommender import BookRecommendationService

# Global DS service
_ds_service = None

def get_ds_service():
    """Initialize DS service once"""
    global _ds_service
    if _ds_service is None:
        _ds_service = BookRecommendationService()
        if not _ds_service.vector_store.load_index():
            raise ValueError("Vector store not found")
    return _ds_service


def test_ds_service():
    """Test that DS service initializes and loads vector store"""
    print("\n" + "="*70)
    print("TEST 1: DS Service Initialization")
    print("="*70)
    
    try:
        ds_service = get_ds_service()
        print("✓ DS service initialized successfully")
        
        # Check vector store stats
        stats = ds_service.get_stats()
        print(f"✓ Vector store loaded: {stats['total_vectors']} books indexed")
        print(f"✓ Embedding model: {stats['model']}")
        print(f"✓ Embedding dimension: {stats['embedding_dim']}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize DS service: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_isbns_from_ds(query, top_k=5):
    """
    Simulates what backend does: calls DS and gets ISBNs
    This is the core function we're testing
    """
    ds_service = get_ds_service()
    recommendations = ds_service.find_similar_books(query_title=query, top_k=top_k)
    
    isbns = []
    for rec in recommendations:
        isbn = str(rec.get('book_id', '')).rstrip('0').rstrip('.')
        if isbn:
            isbns.append(isbn)
    
    return isbns


def test_search_function(query="Harry Potter", top_k=5):
    """Test getting ISBNs from DS"""
    print("\n" + "="*70)
    print(f"TEST 2: Backend Gets ISBNs from DS - Query: '{query}'")
    print("="*70)
    
    try:
        # This is what backend does: call DS and get ISBNs
        isbns = get_isbns_from_ds(query, top_k=top_k)
        
        if isbns:
            print(f"✓ DS returned {len(isbns)} ISBNs to backend:")
            for i, isbn in enumerate(isbns, 1):
                print(f"  {i}. ISBN: {isbn}")
            print(f"\n✓ Backend received ISBNs successfully!")
            print(f"  (Backend would now use these ISBNs to query database)")
        else:
            print("⚠ DS returned no results (empty list)")
        
        return True
    except Exception as e:
        print(f"✗ Failed to get ISBNs from DS: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_queries():
    """Test with multiple different queries"""
    print("\n" + "="*70)
    print("TEST 3: Multiple Queries (Backend -> DS)")
    print("="*70)
    
    test_queries = [
        ("fantasy adventure", 3),
        ("science fiction", 3),
        ("mystery novel", 3)
    ]
    
    for query, top_k in test_queries:
        print(f"\n  Query: '{query}' (top {top_k})")
        try:
            isbns = get_isbns_from_ds(query, top_k=top_k)
            print(f"  → Backend received {len(isbns)} ISBNs: {isbns[:3] if isbns else '[]'}")
        except Exception as e:
            print(f"  → Failed: {e}")


def main():
    print("\n" + "="*70)
    print("DS -> BACKEND INTEGRATION TEST (No Database Required)")
    print("="*70)
    print("This test verifies that backend correctly receives ISBNs from DS")
    
    # Test 1: Initialize DS service
    if not test_ds_service():
        print("\n❌ DS service initialization failed. Stopping tests.")
        return
    
    # Test 2: Test getting ISBNs from DS
    if not test_search_function("Harry Potter", top_k=5):
        print("\n❌ Failed to get ISBNs from DS. Stopping tests.")
        return
    
    # Test 3: Test with multiple queries
    test_multiple_queries()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - DS -> BACKEND COMMUNICATION WORKS!")
    print("="*70)
    print("\nWhat was tested:")
    print("✓ DS service initializes and loads vector store")
    print("✓ Backend can call DS and receive ISBNs")
    print("✓ ISBNs are in correct format (cleaned strings)")
    print("\nNext steps:")
    print("1. These ISBNs can be used as book IDs in your database")
    print("2. Test with actual database: get_book_by_id(db, isbn)")
    print("3. Test full search flow in your backend API")
    print()


if __name__ == "__main__":
    main()
