#!/usr/bin/env python3
"""
Simple database fix script
"""

from app import app, db
from models import *
import sys

def fix_database():
    """Fix the database by recreating all tables"""
    with app.app_context():
        try:
            print("Fixing database...")
            
            # Create all tables (this will create missing tables and columns)
            db.create_all()
            
            print("Database fixed successfully!")
            
        except Exception as e:
            print(f"Fix failed: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    fix_database()