import logging
import sys
import os
from fastapi import FastAPI
from routers import auth, books, ratings
from starlette.middleware.sessions import SessionMiddleware
from core.config import API_SECRET_KEY

sys.path.append(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific logger levels
logging.getLogger('uvicorn').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('fastapi').setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Starting BookFinder API...")

app = FastAPI(
    title="BookFinder API",
    description="API for BookFinder app",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"  # OpenAPI JSON
)
app.add_middleware(SessionMiddleware, secret_key=API_SECRET_KEY)

# Startup event to preload DS service
@app.on_event("startup")
async def startup_event():
    """Preload the DS service and vector store on startup"""
    logger.info("Preloading Data Science service and vector store...")
    try:
        from services.books_service import _get_ds_service
        _get_ds_service()
        logger.info("✓ DS service preloaded successfully")
    except Exception as e:
        logger.error(f"✗ Failed to preload DS service: {e}")
        logger.warning("DS service will be loaded on first search request")

app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/api")
app.include_router(ratings.router, prefix="/api")

@app.get("/")
def root():
    logger.debug("Root endpoint called")
    return {"message": "API running"}