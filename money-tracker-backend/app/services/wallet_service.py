from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.wallet import Wallet, WalletTransfer, BalanceAdjustment
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.wallet import (
    WalletCreate, WalletUpdate, WalletTransferCreate, BalanceAdjustmentCreate,
    WalletAnalytics
)
from fastapi import HTTPException

class WalletService:
    """Service class for wallet operations."""
    
    @staticmethod
    def create_wallet(db: Session, wallet_data: WalletCreate, user: User) -> Wallet:
        """Create a new wallet for the user."""
        # If this is the first wallet or marked as default, make it default
        existing_wallets = db.query(Wallet).filter(
            and_(Wallet.user_id == user.id, Wallet.is_active == True)
        ).count()
        
        is_default = wallet_data.is_default or existing_wallets == 0
        
        # If setting as default, remove default from other wallets
        if is_default:
            db.query(Wallet).filter(
                and_(Wallet.user_id == user.id, Wallet.is_default == True)
            ).update({"is_default": False})
        
        wallet = Wallet(
            name=wallet_data.name,
            wallet_type=wallet_data.wallet_type.value,
            icon=wallet_data.icon,
            color=wallet_data.color,
            balance=wallet_data.initial_balance or 0.0,
            description=wallet_data.description,
            is_default=is_default,
            user_id=user.id
        )
        
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet
    
    @staticmethod
    def get_wallets(db: Session, user: User, include_inactive: bool = False) -> List[Wallet]:
        """Get all wallets for a user."""
        query = db.query(Wallet).filter(Wallet.user_id == user.id)
        
        if not include_inactive:
            query = query.filter(Wallet.is_active == True)
        
        return query.order_by(Wallet.is_default.desc(), Wallet.created_at.desc()).all()
    
    @staticmethod
    def get_wallet(db: Session, wallet_id: int, user: User) -> Wallet:
        """Get a specific wallet."""
        wallet = db.query(Wallet).filter(
            and_(Wallet.id == wallet_id, Wallet.user_id == user.id)
        ).first()
        
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        return wallet
    
    @staticmethod
    def update_wallet(db: Session, wallet_id: int, wallet_update: WalletUpdate, user: User) -> Wallet:
        """Update a wallet."""
        wallet = WalletService.get_wallet(db, wallet_id, user)
        
        # If setting as default, remove default from other wallets
        if wallet_update.is_default:
            db.query(Wallet).filter(
                and_(Wallet.user_id == user.id, Wallet.is_default == True, Wallet.id != wallet_id)
            ).update({"is_default": False})
        
        # Update fields
        update_data = wallet_update.dict(exclude_unset=True)
        if wallet_update.wallet_type:
            update_data["wallet_type"] = wallet_update.wallet_type.value
        
        for field, value in update_data.items():
            setattr(wallet, field, value)
        
        wallet.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(wallet)
        return wallet
    
    @staticmethod
    def delete_wallet(db: Session, wallet_id: int, user: User) -> bool:
        """Soft delete a wallet (mark as inactive)."""
        wallet = WalletService.get_wallet(db, wallet_id, user)
        
        # Check if wallet has transactions
        transaction_count = db.query(Transaction).filter(Transaction.wallet_id == wallet_id).count()
        if transaction_count > 0:
            # Soft delete - mark as inactive
            wallet.is_active = False
            wallet.updated_at = datetime.utcnow()
        else:
            # Hard delete if no transactions
            db.delete(wallet)
        
        # If this was the default wallet, make another wallet default
        if wallet.is_default:
            other_wallet = db.query(Wallet).filter(
                and_(Wallet.user_id == user.id, Wallet.is_active == True, Wallet.id != wallet_id)
            ).first()
            if other_wallet:
                other_wallet.is_default = True
        
        db.commit()
        return True
    
    @staticmethod
    def transfer_money(db: Session, transfer_data: WalletTransferCreate, user: User) -> WalletTransfer:
        """Transfer money between wallets."""
        # Validate wallets
        from_wallet = WalletService.get_wallet(db, transfer_data.from_wallet_id, user)
        to_wallet = WalletService.get_wallet(db, transfer_data.to_wallet_id, user)
        
        if from_wallet.id == to_wallet.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to the same wallet")
        
        if from_wallet.balance < transfer_data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance in source wallet")
        
        # Create transfer record
        transfer = WalletTransfer(
            from_wallet_id=transfer_data.from_wallet_id,
            to_wallet_id=transfer_data.to_wallet_id,
            amount=transfer_data.amount,
            description=transfer_data.description,
            transfer_date=transfer_data.transfer_date or datetime.utcnow(),
            user_id=user.id
        )
        
        # Update wallet balances
        from_wallet.balance -= transfer_data.amount
        to_wallet.balance += transfer_data.amount
        from_wallet.updated_at = datetime.utcnow()
        to_wallet.updated_at = datetime.utcnow()
        
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer
    
    @staticmethod
    def adjust_balance(db: Session, adjustment_data: BalanceAdjustmentCreate, user: User) -> BalanceAdjustment:
        """Manually adjust wallet balance for reconciliation."""
        wallet = WalletService.get_wallet(db, adjustment_data.wallet_id, user)
        
        old_balance = wallet.balance
        adjustment_amount = adjustment_data.new_balance - old_balance
        
        adjustment = BalanceAdjustment(
            wallet_id=adjustment_data.wallet_id,
            old_balance=old_balance,
            new_balance=adjustment_data.new_balance,
            adjustment_amount=adjustment_amount,
            reason=adjustment_data.reason,
            user_id=user.id
        )
        
        # Update wallet balance
        wallet.balance = adjustment_data.new_balance
        wallet.updated_at = datetime.utcnow()
        
        db.add(adjustment)
        db.commit()
        db.refresh(adjustment)
        return adjustment
    
    @staticmethod
    def get_wallet_analytics(db: Session, wallet_id: int, user: User, days: int = 30) -> WalletAnalytics:
        """Get analytics for a specific wallet."""
        wallet = WalletService.get_wallet(db, wallet_id, user)
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get transactions for the period
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.wallet_id == wallet_id,
                Transaction.user_id == user.id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).all()
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
        net_change = total_income - total_expenses
        transaction_count = len(transactions)
        avg_transaction = (total_income + total_expenses) / transaction_count if transaction_count > 0 else 0
        
        return WalletAnalytics(
            wallet_id=wallet.id,
            wallet_name=wallet.name,
            total_income=total_income,
            total_expenses=total_expenses,
            net_change=net_change,
            transaction_count=transaction_count,
            avg_transaction_amount=avg_transaction,
            balance=wallet.balance
        )
    
    @staticmethod
    def get_wallet_history(db: Session, wallet_id: int, user: User, skip: int = 0, limit: int = 50) -> dict:
        """Get transaction history for a specific wallet."""
        wallet = WalletService.get_wallet(db, wallet_id, user)
        
        # Get transactions with pagination
        transactions_query = db.query(Transaction).filter(
            and_(Transaction.wallet_id == wallet_id, Transaction.user_id == user.id)
        ).order_by(Transaction.date.desc())
        
        total_count = transactions_query.count()
        transactions = transactions_query.offset(skip).limit(limit).all()
        
        return {
            "wallet": wallet,
            "transactions": transactions,
            "total_count": total_count,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "limit": limit
        }
    
    @staticmethod
    def get_default_wallet(db: Session, user: User) -> Optional[Wallet]:
        """Get user's default wallet."""
        return db.query(Wallet).filter(
            and_(Wallet.user_id == user.id, Wallet.is_default == True, Wallet.is_active == True)
        ).first()
    
    @staticmethod
    def update_wallet_balance(db: Session, wallet_id: int, amount: float, transaction_type: str):
        """Update wallet balance when a transaction is created/updated/deleted."""
        wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if wallet:
            if transaction_type == "income":
                wallet.balance += amount
            elif transaction_type == "expense":
                wallet.balance -= amount
            
            wallet.updated_at = datetime.utcnow()
            db.commit()
