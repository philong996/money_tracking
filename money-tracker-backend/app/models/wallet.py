from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Wallet(Base):
    """Wallet database model."""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    wallet_type = Column(String, nullable=False)  # cash, bank_account, credit_card, savings, investment
    icon = Column(String, default="wallet")  # icon identifier
    color = Column(String, default="#4F46E5")  # hex color code
    balance = Column(Float, default=0.0)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")
    
    # For wallet transfers
    transfers_from = relationship(
        "WalletTransfer", 
        foreign_keys="WalletTransfer.from_wallet_id",
        back_populates="from_wallet"
    )
    transfers_to = relationship(
        "WalletTransfer", 
        foreign_keys="WalletTransfer.to_wallet_id",
        back_populates="to_wallet"
    )

class WalletTransfer(Base):
    """Wallet transfer database model for tracking money transfers between wallets."""
    __tablename__ = "wallet_transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    transfer_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    from_wallet_id = Column(Integer, ForeignKey("wallets.id"))
    to_wallet_id = Column(Integer, ForeignKey("wallets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    from_wallet = relationship("Wallet", foreign_keys=[from_wallet_id], back_populates="transfers_from")
    to_wallet = relationship("Wallet", foreign_keys=[to_wallet_id], back_populates="transfers_to")
    owner = relationship("User")

class BalanceAdjustment(Base):
    """Balance adjustment model for manual reconciliation."""
    __tablename__ = "balance_adjustments"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    old_balance = Column(Float, nullable=False)
    new_balance = Column(Float, nullable=False)
    adjustment_amount = Column(Float, nullable=False)
    reason = Column(String)
    adjusted_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    wallet = relationship("Wallet")
    user = relationship("User")
