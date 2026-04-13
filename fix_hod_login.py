#!/usr/bin/env python3
"""
Quick Fix HOD Login
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def fix_hod_login():
    """Fix HOD login issue"""
    db_path = 'instance/faculty_workload.db'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Set password
        hashed_password = generate_password_hash('hod123')
        
        # Delete any existing A.B.Bhatlawande first
        cursor.execute("DELETE FROM user WHERE username = 'A.S.Bhatlawande'")
        
        # Create fresh HOD account
        cursor.execute("""
            INSERT INTO user (username, password_hash, role, full_name, is_active) 
            VALUES (?, ?, 'hod', 'A.S.Bhatlawande', 1)
        """, ('A.S.Bhatlawande', hashed_password))
        
        # Make M.B.Patil faculty if exists
        cursor.execute("UPDATE user SET role = 'faculty' WHERE username = 'M.B.Patil'")
        
        conn.commit()
        print("✅ HOD Fixed!")
        print("Username: A.S.Bhatlawande")
        print("Password: hod123")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_hod_login()
