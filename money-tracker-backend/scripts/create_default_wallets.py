"""
Script to create a default wallet for existing users in the database.
Run this after adding the wallet functionality to ensure existing users have a default wallet.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.user import User
from app.models.wallet import Wallet

def create_default_wallets():
    """Create default wallets for all existing users."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get all users who don't have wallets
        users_without_wallets = db.query(User).filter(
            ~User.id.in_(db.query(Wallet.user_id).distinct())
        ).all()
        
        for user in users_without_wallets:
            default_wallet = Wallet(
                name="Main Wallet",
                wallet_type="cash",
                icon="wallet",
                color="#4F46E5",
                balance=0.0,
                is_default=True,
                is_active=True,
                description="Default wallet created automatically",
                user_id=user.id
            )
            db.add(default_wallet)
            print(f"Created default wallet for user: {user.username}")
        
        db.commit()
        print(f"Successfully created default wallets for {len(users_without_wallets)} users")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating default wallets: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_wallets()
