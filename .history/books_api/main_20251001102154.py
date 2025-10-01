# books_api/main.py
from fastapi import FastAPI
from books_api.presentation.routes import router

app = FastAPI(title="Books API")

app.include_router(router)
