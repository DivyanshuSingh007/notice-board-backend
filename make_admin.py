#!/usr/bin/env python3
"""
Script to make a user admin in the database
Usage: python make_admin.py <email>
"""

import sys
from sqlalchemy.orm import Session
from db import Sessionlocal
from models import Users

def make_user_admin(email: str):
    """Make a user admin by their email"""
    db = Sessionlocal()
    try:
        # Find the user by email
        user = db.query(Users).filter(Users.email == email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found!")
            return False
        
        # Update admin status
        user.admin = True
        db.commit()
        
        print(f"✅ Successfully made user '{email}' an admin!")
        print(f"   User ID: {user.id}")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Admin: {user.admin}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_all_users():
    """List all users in the database"""
    db = Sessionlocal()
    try:
        users = db.query(Users).all()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print("📋 All users in database:")
        print("-" * 50)
        for user in users:
            admin_status = "👑 ADMIN" if user.admin else "👤 USER"
            print(f"ID: {user.id} | {admin_status}")
            print(f"Email: {user.email}")
            print(f"Name: {user.first_name} {user.last_name}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <email>")
        print("   or: python make_admin.py --list (to see all users)")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_all_users()
    else:
        email = sys.argv[1]
        make_user_admin(email) 