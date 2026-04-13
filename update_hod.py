#!/usr/bin/env python3
"""
Update HOD Script
Changes M.B.Patil to A.B.Bhatlawande as HOD
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def update_hod():
    """Update HOD from M.B.Patil to A.B.Bhatlawande"""
    db_path = 'instance/faculty_workload.db'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # First, check all existing users
        cursor.execute("SELECT username, role, is_active FROM user")
        all_users = cursor.fetchall()
        print("Current users in database:")
        for user in all_users:
            print(f"  {user[0]} - {user[1]} - {'Active' if user[2] else 'Inactive'}")
        
        # Set new password for HOD
        hashed_password = generate_password_hash('hodpass')
        
        # Check if A.B.Bhatlawande already exists
        cursor.execute("SELECT * FROM user WHERE username = 'A.B.Bhatlawande'")
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Update existing A.B.Bhatlawande to be active HOD with new password
            cursor.execute("""
                UPDATE user 
                SET role = 'hod',
                    password_hash = ?,
                    full_name = 'A.B.Bhatlawande',
                    is_active = 1
                WHERE username = 'A.B.Bhatlawande'
            """, (hashed_password,))
            print("Updated A.B.Bhatlawande: set as HOD, activated account, reset password")
            
            # Update M.B.Patil to faculty if exists
            cursor.execute("""
                UPDATE user 
                SET role = 'faculty'
                WHERE username = 'M.B.Patil'
            """)
            print("Changed M.B.Patil from HOD to faculty")
        else:
            # Check if M.B.Patil exists and update to A.B.Bhatlawande
            cursor.execute("SELECT * FROM user WHERE username = 'M.B.Patil'")
            old_hod = cursor.fetchone()
            
            if old_hod:
                cursor.execute("""
                    UPDATE user 
                    SET username = 'A.B.Bhatlawande',
                        password_hash = ?,
                        full_name = 'A.B.Bhatlawande',
                        is_active = 1
                    WHERE username = 'M.B.Patil'
                """, (hashed_password,))
                print("Updated M.B.Patil to A.B.Bhatlawande with new password and activated")
            else:
                # Create new HOD
                cursor.execute("""
                    INSERT INTO user (username, password_hash, role, full_name, is_active, date_joined)
                    VALUES (?, ?, 'hod', ?, 1, datetime('now'))
                """, ('A.B.Bhatlawande', hashed_password, 'A.B.Bhatlawande'))
                print("Created new HOD: A.B.Bhatlawande")
        
        conn.commit()
        print("HOD update completed successfully!")
        print("\n=== HOD Login Credentials ===")
        print("Username: A.B.Bhatlawande")
        print("Password: hodpass")
        print("==============================\n")
        
        # Show current HOD
        cursor.execute("SELECT username, role FROM user WHERE role = 'hod'")
        current_hod = cursor.fetchone()
        if current_hod:
            print(f"Current HOD: {current_hod[0]}")
        
    except Exception as e:
        print(f"Error updating HOD: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_hod()
