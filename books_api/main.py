from fastapi import FastAPI
from books_api.presentation.routes import router
"""
Main entry point for the Book API application.

This module creates a FastAPI application instance and includes the API router.
"""
app = FastAPI(title="Book API")

app.include_router(router)
