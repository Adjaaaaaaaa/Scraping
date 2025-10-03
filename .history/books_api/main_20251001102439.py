# books_api/main.py
from fastapi import FastAPI
from books_api.presentation.routes import router

app = FastAPI(title="Book API")

app.include_router(router)
