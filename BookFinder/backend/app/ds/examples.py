"""
Example: How to use the DS Book Recommendation System with Pre-built Vector Store
This demonstrates using the FAISS index built from book_description.csv
"""

from app import BookRecommendationService
from pathlib import Path


def real_world_example():
    """
    Real-world example using pre-built vector store
    
    Prerequisites:
    - Vector store already built in ./vector_stores/
    - Run build_vector_store.py first if not already done
    """
    print("\n" + "="*70)
    print("🚀 BOOK RECOMMENDATION - REAL WORLD EXAMPLE")
    print("="*70 + "\n")
    
    # Check if vector store exists
    vector_store_path = Path(__file__).parent / "vector_stores" / "books.faiss"
    
    if not vector_store_path.exists():
        print("❌ ERROR: Vector store not found!")
        print("\nPlease run the build script first:")
        print("  python build_vector_store.py")
        print("\nThis will create:")
        print("  - vector_stores/books.faiss")
        print("  - vector_stores/books_metadata.json")
        return
    
    print("✅ Found pre-built vector store")
    print(f"   Location: {vector_store_path}")
    print()
    
    # 1. Initialize the service
    print("📚 Initializing Book Recommendation Service...")
    service = BookRecommendationService()
    
    # The service will automatically load the pre-built vector store
    # from vector_stores/books.faiss and books_metadata.json
    
    # 2. Get statistics
    stats = service.get_stats()
    print(f"\n📊 Vector Store Statistics:")
    print(f"   Model: {stats['model']}")
    print(f"   Embedding Dimension: {stats['embedding_dim']}")
    print(f"   Total Books Indexed: {stats['total_vectors']}")
    print(f"   Index Loaded: {stats['index_exists']}")
    print()
    
    # 3. Try different search queries
    test_queries = [
        ("Harry Potter", 5),
        ("Science fiction adventure", 5),
        ("Classic literature novel", 3),
    ]
    
    for query_title, top_k in test_queries:
        print("─" * 70)
        print(f"🔍 Searching for: '{query_title}' (top {top_k})")
        print("─" * 70)
        
        try:
            # Find similar books
            recommendations = service.find_similar_books(
                query_title=query_title,
                top_k=top_k
            )
            
            if not recommendations:
                print("   ⚠️  No recommendations found")
                print()
                continue
            
            # Display results
            print(f"\n   Found {len(recommendations)} recommendations:\n")
            
            for rec in recommendations:
                print(f"   {rec['rank']}. Book ID: {rec['book_id']}")
                print(f"      Title: {rec.get('title', 'N/A')}")
                print(f"      Author: {rec.get('author', 'N/A')}")
                print(f"      Similarity: {rec['similarity_percentage']}% "
                      f"(score: {rec['similarity_score']:.4f})")
                print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    # 4. Cache statistics
    print("─" * 70)
    print("📦 Cache Statistics")
    print("─" * 70)
    cache_stats = service.get_cache_stats()
    print(f"   Total cached descriptions: {cache_stats.get('total_cached', 0)}")
    print(f"   Cache file: {cache_stats.get('cache_file', 'N/A')}")
    print()
    
    print("="*70)
    print("✅ EXAMPLE COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n💡 Tips:")
    print("   - The vector store is loaded ONCE and reused")
    print("   - Query descriptions are cached for faster repeated searches")
    print("   - Book IDs match the ISBN column from your CSV")
    print("   - Similarity scores range from 0.0 to 1.0 (higher = more similar)")
    print()
    print("� Next Steps:")
    print("   - Use these book IDs to fetch full details from your database")
    print("   - Integrate with backend API: GET /recommendations?title=...")
    print("   - The backend will use book IDs to get store info from DB")
    print()


if __name__ == "__main__":
    real_world_example()
