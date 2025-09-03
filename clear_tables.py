#!/usr/bin/env python3
"""
Script to clear all records from users and notice tables
"""
from db import Sessionlocal
from models import Users, Notice
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_all_tables():
    """Delete all records from users and notice tables"""
    db = Sessionlocal()
    try:
        # Clear notices table
        notice_count = db.query(Notice).count()
        db.query(Notice).delete()
        logger.info(f"Deleted {notice_count} notices")
        
        # Clear users table
        user_count = db.query(Users).count()
        db.query(Users).delete()
        logger.info(f"Deleted {user_count} users")
        
        # Commit the changes
        db.commit()
        logger.info("All tables cleared successfully")
        
        # Verify tables are empty
        remaining_notices = db.query(Notice).count()
        remaining_users = db.query(Users).count()
        logger.info(f"Remaining notices: {remaining_notices}")
        logger.info(f"Remaining users: {remaining_users}")
        
    except Exception as e:
        logger.error(f"Error clearing tables: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("⚠️  WARNING: This will delete ALL records from users and notice tables!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm == "YES":
        clear_all_tables()
        print("✅ Tables cleared successfully!")
    else:
        print("❌ Operation cancelled")
