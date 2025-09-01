from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.wallet import (
    WalletCreate, WalletUpdate, WalletResponse, WalletSummary,
    WalletTransferCreate, WalletTransferResponse,
    BalanceAdjustmentCreate, BalanceAdjustmentResponse,
    WalletAnalytics, WalletHistory
)
from app.services.wallet_service import WalletService

router = APIRouter()

@router.post("/wallets", response_model=WalletResponse)
def create_wallet(
    wallet: WalletCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new wallet."""
    return WalletService.create_wallet(db, wallet, current_user)

@router.get("/wallets", response_model=List[WalletResponse])
def get_wallets(
    include_inactive: bool = Query(False, description="Include inactive wallets"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user's wallets."""
    return WalletService.get_wallets(db, current_user, include_inactive)

@router.get("/wallets/summary", response_model=List[WalletSummary])
def get_wallets_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get wallets summary with transaction counts."""
    wallets = WalletService.get_wallets(db, current_user)
    summary_list = []
    
    for wallet in wallets:
        transaction_count = len(wallet.transactions)
        summary_list.append(WalletSummary(
            id=wallet.id,
            name=wallet.name,
            wallet_type=wallet.wallet_type,
            icon=wallet.icon,
            color=wallet.color,
            balance=wallet.balance,
            is_default=wallet.is_default,
            is_active=wallet.is_active,
            transaction_count=transaction_count
        ))
    
    return summary_list

@router.get("/wallets/default", response_model=Optional[WalletResponse])
def get_default_wallet(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's default wallet."""
    return WalletService.get_default_wallet(db, current_user)

@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
def get_wallet(
    wallet_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific wallet."""
    return WalletService.get_wallet(db, wallet_id, current_user)

@router.put("/wallets/{wallet_id}", response_model=WalletResponse)
def update_wallet(
    wallet_id: int,
    wallet_update: WalletUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a wallet."""
    return WalletService.update_wallet(db, wallet_id, wallet_update, current_user)

@router.delete("/wallets/{wallet_id}")
def delete_wallet(
    wallet_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a wallet (soft delete if has transactions)."""
    success = WalletService.delete_wallet(db, wallet_id, current_user)
    return {"message": "Wallet deleted successfully" if success else "Failed to delete wallet"}

@router.post("/wallets/transfer", response_model=WalletTransferResponse)
def transfer_money(
    transfer: WalletTransferCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Transfer money between wallets."""
    return WalletService.transfer_money(db, transfer, current_user)

@router.get("/wallets/transfers", response_model=List[WalletTransferResponse])
def get_wallet_transfers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get wallet transfer history."""
    from app.models.wallet import WalletTransfer
    from sqlalchemy import and_
    
    transfers = db.query(WalletTransfer).filter(
        WalletTransfer.user_id == current_user.id
    ).order_by(WalletTransfer.transfer_date.desc()).offset(skip).limit(limit).all()
    
    return transfers

@router.post("/wallets/{wallet_id}/adjust", response_model=BalanceAdjustmentResponse)
def adjust_wallet_balance(
    wallet_id: int,
    adjustment: BalanceAdjustmentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually adjust wallet balance for reconciliation."""
    # Override wallet_id from URL
    adjustment.wallet_id = wallet_id
    return WalletService.adjust_balance(db, adjustment, current_user)

@router.get("/wallets/{wallet_id}/analytics", response_model=WalletAnalytics)
def get_wallet_analytics(
    wallet_id: int,
    days: int = Query(30, ge=1, le=365, description="Number of days for analytics"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific wallet."""
    return WalletService.get_wallet_analytics(db, wallet_id, current_user, days)

@router.get("/wallets/{wallet_id}/history", response_model=WalletHistory)
def get_wallet_history(
    wallet_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get transaction history for a specific wallet."""
    return WalletService.get_wallet_history(db, wallet_id, current_user, skip, limit)

@router.get("/wallets/{wallet_id}/adjustments", response_model=List[BalanceAdjustmentResponse])
def get_balance_adjustments(
    wallet_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get balance adjustment history for a wallet."""
    from app.models.wallet import BalanceAdjustment
    from sqlalchemy import and_
    
    # Verify wallet ownership
    WalletService.get_wallet(db, wallet_id, current_user)
    
    adjustments = db.query(BalanceAdjustment).filter(
        and_(BalanceAdjustment.wallet_id == wallet_id, BalanceAdjustment.user_id == current_user.id)
    ).order_by(BalanceAdjustment.adjusted_at.desc()).offset(skip).limit(limit).all()
    
    return adjustments
