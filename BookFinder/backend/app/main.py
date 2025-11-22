from fastapi import FastAPI
from routers import auth, books, ratings
from starlette.middleware.sessions import SessionMiddleware
from core.config import API_SECRET_KEY
import sys, os
sys.path.append(os.path.dirname(__file__))

app = FastAPI(
    title="BookFinder API",
    description="API for BookFinder app",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"  # OpenAPI JSON
)
app.add_middleware(SessionMiddleware, secret_key=API_SECRET_KEY)

app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/api")
app.include_router(ratings.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API running"}