from fastapi import FastAPI
from books_api.data.database import Base, engine
from books_api.data import models
from books_api.presentation import routes


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API - Clean Architecture")

app.include_router(routes.router)
