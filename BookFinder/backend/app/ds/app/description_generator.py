"""
Description Generator using OpenAI API
Generates book descriptions/plot summaries from titles with caching
"""
import json
import hashlib
import logging
from typing import Optional
from openai import OpenAI
from pathlib import Path

try:
    from .config import config
except ImportError:
    from config import config

# Initialize logger
logger = logging.getLogger(__name__)


class DescriptionGenerator:
    """
    Generates book descriptions using OpenAI API
    Caches results to avoid repeated API calls
    """
    
    PROMPT_TEMPLATE = """You are a warm, clear, and insightful book-description assistant.
Given a book title (in Armenian or English), provide a concise English summary of the book.
Focus on:

the core plot and main themes

the emotional tone and character journeys

the genre and what makes the book meaningful or distinctive

Write in a natural, human-friendly style, but keep the wording straightforward so it can be used for semantic vector embeddings.
Limit the description to under 200 words.

If the exact book is not recognized, describe a closely related book with similar themes, tone, and genre so the result remains relevant for recommendation purposes.

Output only the description. No extra text.

Book Title: {title}"""
    
    def __init__(self):
        """Initialize the description generator with OpenAI client"""
        logger.info("Initializing DescriptionGenerator...")
        
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == 'synthetic-key-replace-with-real-one':
            logger.warning("OpenAI API key not set. Will use mock data.")
            self.client = None
        else:
            logger.info("OpenAI API key found")
            try:
                # Simple initialization - remove timeout and max_retries if causing issues
                self.client = OpenAI(api_key=config.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
                logger.warning("Falling back to mock descriptions")
                self.client = None
        
        self.cache_path = config.get_cache_path('descriptions')
        logger.debug(f"Cache path: {self.cache_path}")
        self.cache = self._load_cache()
        logger.info(f"Loaded {len(self.cache)} cached descriptions")

    def _load_cache(self) -> dict:
        """Load cache from disk"""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            logger.debug(f"Cache saved ({len(self.cache)} entries)")
        except Exception as e:
            logger.warning(f"Could not save cache: {e}")
    
    def _get_cache_key(self, title: str) -> str:
        """Generate a cache key from book title"""
        return hashlib.md5(title.lower().strip().encode()).hexdigest()
    
    def _generate_mock_description(self, title: str) -> str:
        """Generate a mock description when API is not available"""
        return f"A compelling story about {title}. This book explores themes of adventure, " \
               f"personal growth, and the human condition through an engaging narrative."
    
    def generate_description(self, title: str, use_cache: bool = True) -> str:
        """
        Generate a description for a book title
        
        Args:
            title: Book title to generate description for
            use_cache: Whether to use cached results
            
        Returns:
            Generated description string
        """
        logger.info(f"Processing book title: '{title}'")
        
        # Check cache first
        cache_key = self._get_cache_key(title)
        if use_cache and cache_key in self.cache:
            logger.debug(f"Cache HIT for '{title}'")
            cached_desc = self.cache[cache_key]
            logger.debug(f"Description preview: {cached_desc[:100]}...")
            return cached_desc
        
        logger.debug(f"Cache MISS for '{title}' - need to generate")
        
        # If no API client, return mock description
        if self.client is None:
            logger.info(f"Using MOCK description (no API client) for '{title}'")
            description = self._generate_mock_description(title)
            logger.debug(f"Mock description: {description[:100]}...")
            self.cache[cache_key] = description
            self._save_cache()
            return description
        
        # Generate using OpenAI
        try:
            logger.info(f"Calling OpenAI API for '{title}'")
            logger.debug(f"Model: {config.OPENAI_MODEL}, Temperature: {config.OPENAI_TEMPERATURE}")
            
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful book information assistant."
                    },
                    {
                        "role": "user",
                        "content": self.PROMPT_TEMPLATE.format(title=title)
                    }
                ],
                temperature=config.OPENAI_TEMPERATURE,
                max_tokens=config.OPENAI_MAX_TOKENS
            )
            
            description = response.choices[0].message.content.strip()
            
            logger.info(f"OpenAI API response received for '{title}'")
            logger.debug(f"Generated description:\n{'-'*70}\n{description}\n{'-'*70}")
            
            # Cache the result
            self.cache[cache_key] = description
            self._save_cache()
            
            return description
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
            logger.warning(f"Falling back to mock description for '{title}'")
            description = self._generate_mock_description(title)
            logger.debug(f"Mock description: {description[:100]}...")
            return description
    
    def batch_generate_descriptions(self, titles: list[str], use_cache: bool = True) -> dict[str, str]:
        """
        Generate descriptions for multiple titles
        
        Args:
            titles: List of book titles
            use_cache: Whether to use cached results
            
        Returns:
            Dictionary mapping titles to descriptions
        """
        results = {}
        for title in titles:
            results[title] = self.generate_description(title, use_cache)
        return results
    
    def clear_cache(self):
        """Clear the description cache"""
        self.cache = {}
        if self.cache_path.exists():
            self.cache_path.unlink()
        logger.info("Description cache cleared")
    
    def get_cache_stats(self) -> dict:
        """Get statistics about the cache"""
        return {
            "total_cached": len(self.cache),
            "cache_file": str(self.cache_path),
            "cache_exists": self.cache_path.exists()
        }
