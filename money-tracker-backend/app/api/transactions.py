from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse, DashboardData
from app.services.transaction_service import TransactionService

router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction."""
    return TransactionService.create_transaction(db, transaction, current_user)

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's transactions."""
    return TransactionService.get_transactions(db, current_user, skip, limit, category)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific transaction."""
    return TransactionService.get_transaction(db, transaction_id, current_user)

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a transaction."""
    return TransactionService.update_transaction(db, transaction_id, transaction_update, current_user)

@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a transaction."""
    return TransactionService.delete_transaction(db, transaction_id, current_user)

@router.get("/dashboard", response_model=DashboardData)
def get_dashboard_data(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard data."""
    return TransactionService.get_dashboard_data(db, current_user)

@router.get("/categories")
def get_categories():
    """Get available transaction categories."""
    return {
        "categories": ["Food", "Transport", "Shopping", "Entertainment", "Healthcare", "Education", "Other"]
    }

@router.get("/analytics/category-spending")
def get_category_spending(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get category spending analysis."""
    return TransactionService.get_category_spending(db, current_user)
