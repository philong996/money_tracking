from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class WalletType(str, Enum):
    """Enumeration for wallet types."""
    CASH = "cash"
    BANK_ACCOUNT = "bank_account"
    CREDIT_CARD = "credit_card"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    DIGITAL_WALLET = "digital_wallet"

class WalletCreate(BaseModel):
    """Schema for wallet creation."""
    name: str = Field(..., min_length=1, max_length=100)
    wallet_type: WalletType
    icon: Optional[str] = "wallet"
    color: Optional[str] = "#4F46E5"
    initial_balance: Optional[float] = 0.0
    description: Optional[str] = None
    is_default: Optional[bool] = False

class WalletUpdate(BaseModel):
    """Schema for wallet updates."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    wallet_type: Optional[WalletType] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class WalletResponse(BaseModel):
    """Schema for wallet response."""
    id: int
    name: str
    wallet_type: str
    icon: str
    color: str
    balance: float
    is_default: bool
    is_active: bool
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WalletSummary(BaseModel):
    """Schema for wallet summary with transaction count."""
    id: int
    name: str
    wallet_type: str
    icon: str
    color: str
    balance: float
    is_default: bool
    is_active: bool
    transaction_count: int
    
    class Config:
        from_attributes = True

class WalletTransferCreate(BaseModel):
    """Schema for creating wallet transfers."""
    from_wallet_id: int
    to_wallet_id: int
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    transfer_date: Optional[datetime] = None

class WalletTransferResponse(BaseModel):
    """Schema for wallet transfer response."""
    id: int
    amount: float
    description: Optional[str]
    transfer_date: datetime
    created_at: datetime
    from_wallet: WalletResponse
    to_wallet: WalletResponse
    
    class Config:
        from_attributes = True

class BalanceAdjustmentCreate(BaseModel):
    """Schema for creating balance adjustments."""
    wallet_id: int
    new_balance: float
    reason: Optional[str] = None

class BalanceAdjustmentResponse(BaseModel):
    """Schema for balance adjustment response."""
    id: int
    old_balance: float
    new_balance: float
    adjustment_amount: float
    reason: Optional[str]
    adjusted_at: datetime
    wallet: WalletResponse
    
    class Config:
        from_attributes = True

class WalletAnalytics(BaseModel):
    """Schema for wallet analytics."""
    wallet_id: int
    wallet_name: str
    total_income: float
    total_expenses: float
    net_change: float
    transaction_count: int
    avg_transaction_amount: float
    balance: float

class WalletHistory(BaseModel):
    """Schema for wallet transaction history."""
    wallet: WalletResponse
    transactions: List[dict]
    total_count: int
    page: int
    limit: int
