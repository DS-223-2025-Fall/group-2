"""
Vector Store using FAISS
Handles embedding generation, indexing, and similarity search for book descriptions
Loads data from a single CSV file with bookid and description columns
"""
import json
import logging
import numpy as np
import pandas as pd
import faiss
from pathlib import Path
from typing import List, Optional, Tuple
from sentence_transformers import SentenceTransformer

try:
    from .config import config
except ImportError:
    from config import config

# Initialize logger
logger = logging.getLogger(__name__)


class VectorStore:
    """
    Manages FAISS vector index for book descriptions
    Loads data from CSV file with bookid and descr columns
    """
    
    def __init__(self, embedding_model: Optional[str] = None):
        """
        Initialize vector store
        
        Args:
            embedding_model: Name of sentence transformer model to use
        """
        print(f"\n[VectorStore] Initializing vector store...")
        self.model_name = embedding_model or config.EMBEDDING_MODEL
        
        print(f"[VectorStore] Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"[VectorStore] ✓ Model loaded (embedding dim: {self.embedding_dim})")
        
        self.index: Optional[faiss.IndexFlatIP] = None  # Inner Product (for cosine similarity)
        self.metadata: List[dict] = []
        
        self.index_path = config.VECTOR_STORE_PATH / "books.faiss"
        self.metadata_path = config.VECTOR_STORE_PATH / "books_metadata.json"
        print(f"[VectorStore] Index path: {self.index_path}")
        print(f"[VectorStore] Metadata path: {self.metadata_path}\n")
    
    def _normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Normalize embeddings to unit length for cosine similarity
        
        Args:
            embeddings: Array of embeddings
            
        Returns:
            Normalized embeddings
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / (norms + 1e-8)
    
    def create_index(self, descriptions: List[str], metadata: List[dict]):
        """
        Create FAISS index from book descriptions
        
        Args:
            descriptions: List of book descriptions to embed
            metadata: List of metadata dicts (must include 'book_id' field)
        """
        if len(descriptions) != len(metadata):
            raise ValueError("Descriptions and metadata must have same length")
        
        print(f"\n[VectorStore] Creating index for {len(descriptions)} books")
        
        # Generate embeddings
        print(f"[VectorStore] Generating embeddings using {self.model_name}...")
        embeddings = self.model.encode(
            descriptions,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        print(f"[VectorStore] ✓ Generated {len(embeddings)} embeddings")
        
        # Normalize for cosine similarity
        print(f"[VectorStore] Normalizing embeddings for cosine similarity...")
        embeddings = self._normalize_embeddings(embeddings)
        print(f"[VectorStore] ✓ Embeddings normalized")
        
        # Create FAISS index (Inner Product for cosine similarity with normalized vectors)
        print(f"[VectorStore] Creating FAISS index (IndexFlatIP)...")
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings.astype('float32'))
        
        self.metadata = metadata
        
        print(f"[VectorStore] ✓ Index created with {self.index.ntotal} vectors\n")
    
    def save_index(self):
        """Save FAISS index and metadata to disk"""
        if self.index is None:
            raise ValueError("No index to save. Create an index first.")
        
        print(f"\n[VectorStore] Saving index...")
        
        # Ensure directories exist
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(self.index_path))
        print(f"[VectorStore] ✓ Index saved to {self.index_path}")
        
        # Save metadata
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"[VectorStore] ✓ Metadata saved to {self.metadata_path}\n")
    
    def load_index(self) -> bool:
        """
        Load FAISS index and metadata from disk
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.index_path.exists() or not self.metadata_path.exists():
            print(f"[VectorStore] Index files not found")
            return False
        
        try:
            print(f"\n[VectorStore] Loading index from disk...")
            
            # Load FAISS index
            self.index = faiss.read_index(str(self.index_path))
            print(f"[VectorStore] ✓ FAISS index loaded")
            
            # Load metadata
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print(f"[VectorStore] ✓ Metadata loaded")
            
            print(f"[VectorStore] ✓ Loaded index with {self.index.ntotal} vectors\n")
            return True
        
        except Exception as e:
            print(f"[VectorStore] ✗ Error loading index: {e}")
            return False
    
    def search(self, query_description: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """
        Search for similar books using description
        
        Args:
            query_description: Description to search for
            top_k: Number of top results to return
            
        Returns:
            List of tuples (metadata, similarity_score)
        """
        if self.index is None:
            raise ValueError("No index loaded. Load or create an index first.")
        
        print(f"\n[VectorStore] Searching for top {top_k} similar books...")
        print(f"[VectorStore] Query description: {query_description}...")
        
        # Generate query embedding
        print(f"[VectorStore] Generating query embedding...")
        query_embedding = self.model.encode(
            [query_description],
            convert_to_numpy=True
        )
        query_embedding = self._normalize_embeddings(query_embedding)
        print(f"[VectorStore] ✓ Query embedding generated")
        
        # Search
        top_k = min(top_k, self.index.ntotal)
        print(f"[VectorStore] Searching FAISS index...")
        similarities, indices = self.index.search(query_embedding.astype('float32'), top_k)
        print(f"[VectorStore] ✓ Search complete")
        
        # Prepare results
        results = []
        for idx, similarity in zip(indices[0], similarities[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(similarity)))
        
        print(f"[VectorStore] ✓ Returning {len(results)} results\n")
        return results
    
    def load_from_csv(self, csv_path: str, bookid_col: str = 'bookid', descr_col: str = 'descr'):
        """
        Load books from CSV file and create index
        
        Args:
            csv_path: Path to CSV file
            bookid_col: Name of the book ID column (default: 'bookid')
            descr_col: Name of the description column (default: 'descr')
        """
        print(f"\n[VectorStore] Loading data from CSV: {csv_path}")
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        print(f"[VectorStore] ✓ Loaded {len(df)} rows from CSV")
        
        # Validate columns exist
        if bookid_col not in df.columns:
            raise ValueError(f"Column '{bookid_col}' not found in CSV. Available columns: {list(df.columns)}")
        if descr_col not in df.columns:
            raise ValueError(f"Column '{descr_col}' not found in CSV. Available columns: {list(df.columns)}")
        
        # Filter out rows with missing descriptions
        df = df.dropna(subset=[descr_col])
        print(f"[VectorStore] ✓ {len(df)} books with valid descriptions")
        
        # Prepare data
        descriptions = df[descr_col].astype(str).tolist()
        metadata = [{"book_id": str(row[bookid_col])} for _, row in df.iterrows()]
        
        # Create index
        self.create_index(descriptions, metadata)
        
        # Save to disk
        self.save_index()
        
        print(f"[VectorStore] ✓ Index created and saved from CSV\n")
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store"""
        return {
            "model": self.model_name,
            "embedding_dim": self.embedding_dim,
            "total_vectors": self.index.ntotal if self.index else 0,
            "index_exists": self.index_path.exists(),
            "metadata_exists": self.metadata_path.exists()
        }
    
    def add_books(self, descriptions: List[str], metadata: List[dict]):
        """
        Add new books to existing index
        
        Args:
            descriptions: List of new book descriptions
            metadata: List of metadata for new books
        """
        if self.index is None:
            raise ValueError("No index loaded. Load or create an index first.")
        
        if len(descriptions) != len(metadata):
            raise ValueError("Descriptions and metadata must have same length")
        
        print(f"Adding {len(descriptions)} new books to index")
        
        # Generate embeddings
        embeddings = self.model.encode(
            descriptions,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        embeddings = self._normalize_embeddings(embeddings)
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        self.metadata.extend(metadata)
        
        print(f"Index now has {self.index.ntotal} vectors")
    
    def delete_index(self):
        """Delete the index and metadata files"""
        if self.index_path.exists():
            self.index_path.unlink()
        if self.metadata_path.exists():
            self.metadata_path.unlink()
        self.index = None
        self.metadata = []
        print(f"Deleted index files")

