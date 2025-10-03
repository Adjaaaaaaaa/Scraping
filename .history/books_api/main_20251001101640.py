from fastapi import FastAPI
from presentation.routes import router

app = FastAPI(title="Books API")

app.include_router(router)
