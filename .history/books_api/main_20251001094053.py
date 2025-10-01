from fastapi import FastAPI
from books_api.presentation import routes
from books_api.data.database import Base, engine

# Crée les tables si elles n’existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API")

# Inclure les routes
app.include_router(routes.router)
