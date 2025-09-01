"""
Database rebuild script for wallet management schema updates.
This script will drop all existing tables and recreate them with the new schema.

WARNING: This will delete all existing data. Use only in development.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine, Base

def rebuild_database():
    """Drop all tables and recreate with new schema."""
    print("🗑️  Dropping all existing tables...")
    
    # Import all models to ensure they're registered with Base
    from app.models.user import User
    from app.models.transaction import Transaction
    from app.models.wallet import Wallet, WalletTransfer, BalanceAdjustment
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully")
        
        # Recreate all tables with new schema
        print("🔨 Creating tables with new wallet management schema...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully with new schema")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"📋 Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error rebuilding database: {e}")
        raise

if __name__ == "__main__":
    print("🚀 Starting database rebuild for wallet management...")
    print("⚠️  WARNING: This will delete all existing data!")
    
    # Safety confirmation
    response = input("Are you sure you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        exit(1)
    
    rebuild_database()
    print("🎉 Database rebuild completed successfully!")
    print("💡 You can now run the application with the new wallet management schema.")
