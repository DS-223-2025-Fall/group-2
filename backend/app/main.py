from fastapi import FastAPI
from routers import auth, books, ratings
from starlette.middleware.sessions import SessionMiddleware
from core.config import API_SECRET_KEY
import sys, os
sys.path.append(os.path.dirname(__file__))

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=API_SECRET_KEY)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(ratings.router)

@app.get("/")
def root():
    return {"message": "API running"}