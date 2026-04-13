#!/usr/bin/env python3
"""
Remove Sukanya Staff Script
"""

import sqlite3
import os

def remove_sukanya():
    """Remove Sukanya from staff"""
    db_path = 'instance/faculty_workload.db'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if Sukanya exists
        cursor.execute("SELECT * FROM user WHERE username = 'Sukanya'")
        sukanya = cursor.fetchone()
        
        if sukanya:
            print(f"Found user: {sukanya[1]} - {sukanya[3]}")
            
            # Remove Sukanya
            cursor.execute("DELETE FROM user WHERE username = 'Sukanya'")
            
            conn.commit()
            print("✅ Sukanya removed successfully!")
        else:
            print("Sukanya not found in database")
        
        # Show remaining staff
        cursor.execute("SELECT username, role FROM user WHERE role = 'faculty'")
        staff = cursor.fetchall()
        print(f"\nRemaining faculty members: {len(staff)}")
        for member in staff:
            print(f"  - {member[0]}")
            
    except Exception as e:
        print(f"Error removing Sukanya: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    remove_sukanya()
