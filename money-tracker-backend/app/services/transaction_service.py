from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.wallet_service import WalletService

class TransactionService:
    """Service for transaction-related operations."""
    
    @staticmethod
    def create_transaction(db: Session, transaction: TransactionCreate, user: User) -> Transaction:
        """Create a new transaction."""
        # If no wallet specified, use default wallet
        wallet_id = transaction.wallet_id
        if not wallet_id:
            default_wallet = WalletService.get_default_wallet(db, user)
            if default_wallet:
                wallet_id = default_wallet.id
        
        db_transaction = Transaction(
            amount=transaction.amount,
            category=transaction.category,
            description=transaction.description,
            transaction_type=transaction.transaction_type,
            date=transaction.date,
            wallet_id=wallet_id,
            user_id=user.id
        )
        
        db.add(db_transaction)
        db.commit()
        
        # Update wallet balance
        if wallet_id:
            WalletService.update_wallet_balance(
                db, wallet_id, transaction.amount, transaction.transaction_type
            )
        
        db.refresh(db_transaction)
        return db_transaction
    
    @staticmethod
    def get_transactions(
        db: Session, 
        user: User, 
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None
    ) -> List[Transaction]:
        """Get user's transactions with optional filtering."""
        query = db.query(Transaction).filter(Transaction.user_id == user.id)
        if category:
            query = query.filter(Transaction.category == category)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_transaction(db: Session, transaction_id: int, user: User) -> Transaction:
        """Get a specific transaction."""
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user.id
        ).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    @staticmethod
    def update_transaction(
        db: Session, 
        transaction_id: int, 
        transaction_update: TransactionUpdate, 
        user: User
    ) -> Transaction:
        """Update a transaction."""
        transaction = TransactionService.get_transaction(db, transaction_id, user)
        
        # Store old values for wallet balance adjustment
        old_amount = transaction.amount
        old_type = transaction.transaction_type
        old_wallet_id = transaction.wallet_id
        
        # Update transaction fields
        for field, value in transaction_update.dict(exclude_unset=True).items():
            setattr(transaction, field, value)
        
        db.commit()
        
        # Update wallet balances
        if old_wallet_id:
            # Reverse old transaction effect
            reverse_amount = old_amount
            reverse_type = "expense" if old_type == "income" else "income"
            WalletService.update_wallet_balance(db, old_wallet_id, reverse_amount, reverse_type)
        
        # Apply new transaction effect
        new_wallet_id = transaction.wallet_id
        if new_wallet_id:
            WalletService.update_wallet_balance(
                db, new_wallet_id, transaction.amount, transaction.transaction_type
            )
        
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def delete_transaction(db: Session, transaction_id: int, user: User) -> dict:
        """Delete a transaction."""
        transaction = TransactionService.get_transaction(db, transaction_id, user)
        
        # Update wallet balance (reverse the transaction)
        if transaction.wallet_id:
            reverse_type = "expense" if transaction.transaction_type == "income" else "income"
            WalletService.update_wallet_balance(
                db, transaction.wallet_id, transaction.amount, reverse_type
            )
        
        db.delete(transaction)
        db.commit()
        return {"message": "Transaction deleted successfully"}
    
    @staticmethod
    def get_dashboard_data(db: Session, user: User) -> dict:
        """Get dashboard data for user."""
        transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
        balance = total_income - total_expenses
        
        recent_transactions = db.query(Transaction).filter(
            Transaction.user_id == user.id
        ).order_by(Transaction.created_at.desc()).limit(5).all()
        
        # Monthly summary
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_transactions = [
            t for t in transactions 
            if t.date.month == current_month and t.date.year == current_year
        ]
        
        monthly_income = sum(t.amount for t in monthly_transactions if t.transaction_type == "income")
        monthly_expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == "expense")
        
        return {
            "balance": balance,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "recent_transactions": recent_transactions,
            "monthly_summary": {
                "income": monthly_income,
                "expenses": monthly_expenses,
                "net": monthly_income - monthly_expenses
            }
        }
    
    @staticmethod
    def get_category_spending(db: Session, user: User) -> dict:
        """Get category spending analysis."""
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.transaction_type == "expense"
        ).all()
        
        category_spending = {}
        for transaction in transactions:
            category = transaction.category
            if category in category_spending:
                category_spending[category] += transaction.amount
            else:
                category_spending[category] = transaction.amount
        
        return {"data": category_spending}
