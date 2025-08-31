"""
Main entry point for the Money Tracker API.

This application has been split into multiple modules for better organization:

- app/core/: Core configuration, database, and security
- app/models/: SQLAlchemy database models  
- app/schemas/: Pydantic models for request/response validation
- app/services/: Business logic layer
- app/api/: API route handlers

To run the application, you can use: python main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.core.database import create_tables
from app.api import auth, transactions

# Create FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["authentication"])
app.include_router(transactions.router, tags=["transactions"])

# Create database tables
create_tables()

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Money Tracker API", "version": settings.APP_VERSION}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
