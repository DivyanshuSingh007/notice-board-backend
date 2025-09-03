#!/usr/bin/env python3
"""
Script to display all data from users and notice tables
"""
from db import Sessionlocal
from models import Users, Notice
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_all_data():
    """Display all records from users and notice tables"""
    db = Sessionlocal()
    try:
        print("=" * 50)
        print("USERS TABLE")
        print("=" * 50)
        
        users = db.query(Users).all()
        if not users:
            print("No users found")
        else:
            print(f"Total users: {len(users)}")
            for user in users:
                print(f"ID: {user.id}")
                print(f"  Email: {user.email}")
                print(f"  Name: {user.first_name} {user.last_name}")
                print(f"  Mobile: {user.mobile_no}")
                print(f"  Admin: {user.admin}")
                print(f"  Password Hash: {user.hashed_password[:20]}..." if user.hashed_password else "  Password Hash: None")
                print("-" * 30)
        
        print("\n" + "=" * 50)
        print("NOTICE TABLE")
        print("=" * 50)
        
        notices = db.query(Notice).all()
        if not notices:
            print("No notices found")
        else:
            print(f"Total notices: {len(notices)}")
            for notice in notices:
                print(f"ID: {notice.id}")
                print(f"  Title: {notice.title}")
                print(f"  Description: {notice.description}")
                print(f"  Post Date: {notice.post_date}")
                print(f"  Event Date: {notice.event_date}")
                print(f"  Event Start Time: {notice.event_start_time}")
                print(f"  Event End Time: {notice.event_end_time}")
                print(f"  Type: {notice.type}")
                print("-" * 30)
                
    except Exception as e:
        logger.error(f"Error displaying data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    show_all_data()
