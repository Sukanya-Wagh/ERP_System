#!/usr/bin/env python3
"""
Check Users Script
Shows all users in the database
"""

import sqlite3
import os

def check_users():
    """Check all users in the database"""
    db_path = 'instance/faculty_workload.db'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, role, is_active FROM user")
        users = cursor.fetchall()
        
        print("=== All Users in Database ===")
        for user in users:
            username, role, is_active = user
            status = "Active" if is_active else "Inactive"
            print(f"Username: {username} | Role: {role} | Status: {status}")
        
        print("\n=== HOD Users ===")
        cursor.execute("SELECT username, role, is_active FROM user WHERE role = 'hod'")
        hod_users = cursor.fetchall()
        
        for user in hod_users:
            username, role, is_active = user
            status = "Active" if is_active else "Inactive"
            print(f"HOD: {username} | Status: {status}")
            
    except Exception as e:
        print(f"Error checking users: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_users()
