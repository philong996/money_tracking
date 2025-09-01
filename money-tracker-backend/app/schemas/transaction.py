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
    wallet_id: Optional[int] = None  # Allow null for backward compatibility

class TransactionUpdate(BaseModel):
    """Schema for transaction update."""
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    date: Optional[datetime] = None
    wallet_id: Optional[int] = None

class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    amount: float
    category: str
    description: str
    transaction_type: str
    date: datetime
    created_at: datetime
    wallet_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    """Schema for dashboard data."""
    balance: float
    total_income: float
    total_expenses: float
    recent_transactions: List[TransactionResponse]
    monthly_summary: dict
