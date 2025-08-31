from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TransactionCreate(BaseModel):
    """Schema for transaction creation."""
    amount: float
    category: str
    description: str
    transaction_type: str  # "income" or "expense"
    date: datetime

class TransactionUpdate(BaseModel):
    """Schema for transaction update."""
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    date: Optional[datetime] = None

class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    amount: float
    category: str
    description: str
    transaction_type: str
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    """Schema for dashboard data."""
    balance: float
    total_income: float
    total_expenses: float
    recent_transactions: List[TransactionResponse]
    monthly_summary: dict
