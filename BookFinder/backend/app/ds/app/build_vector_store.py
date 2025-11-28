#!/usr/bin/env python3
"""
Build Vector Store from CSV
Run this once to create the vector store, then it will be reused
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from vector_store import VectorStore

def main():
    """Build vector store from CSV file"""
    
    # Configuration - UPDATE THESE for your actual CSV
    CSV_PATH = "../../../../etl/data/book.csv"  # Path from backend/app/ds/app to etl/data/book.csv
    BOOKID_COLUMN = "ISBN"                       # ← Column name for book ID
    DESCR_COLUMN = "description"                 # ← Column name for description
    
    print("="*70)
    print("BUILDING VECTOR STORE FROM CSV")
    print("="*70)
    print(f"CSV Path: {CSV_PATH}")
    print(f"Book ID Column: {BOOKID_COLUMN}")
    print(f"Description Column: {DESCR_COLUMN}")
    print("="*70)
    
    # Check if CSV exists
    csv_file = Path(CSV_PATH)
    if not csv_file.exists():
        print(f"\n❌ ERROR: CSV file not found at: {CSV_PATH}")
        print("Please update CSV_PATH in this script to point to your actual CSV file")
        return 1
    
    try:
        # Initialize vector store
        print("\nInitializing VectorStore...")
        vector_store = VectorStore()
        
        # Load from CSV (this will automatically create and save the index)
        print("\nLoading data from CSV and building index...")
        vector_store.load_from_csv(
            csv_path=str(csv_file),
            bookid_col=BOOKID_COLUMN,
            descr_col=DESCR_COLUMN
        )
        
        # Show stats
        stats = vector_store.get_stats()
        print("\n" + "="*70)
        print("✅ VECTOR STORE BUILT SUCCESSFULLY!")
        print("="*70)
        print(f"Model: {stats['model']}")
        print(f"Embedding Dimension: {stats['embedding_dim']}")
        print(f"Total Vectors: {stats['total_vectors']}")
        print(f"Index File: {stats['index_exists']}")
        print(f"Metadata File: {stats['metadata_exists']}")
        print("="*70)
        
        print("\n📁 Files created:")
        print(f"   - ./vector_stores/books.faiss")
        print(f"   - ./vector_stores/books_metadata.json")
        
        print("\n🎉 Done! The vector store is ready to use.")
        print("   Copy the vector_stores/ directory to your Docker container")
        print("   and the DS service will automatically load it on startup.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to build vector store")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
