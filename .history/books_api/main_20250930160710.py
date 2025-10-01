from fastapi import FastAPI
from data.database import Base, engine
from data import models
from presentation import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API - Clean Architecture")

app.include_router(routes.router)
