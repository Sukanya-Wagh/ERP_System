#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def check_users():
    with app.app_context():
        try:
            users = User.query.all()
            print(f"Total users in database: {len(users)}")
            print("\nUser roles breakdown:")
            
            roles = {}
            for user in users:
                role = user.role
                if role in roles:
                    roles[role] += 1
                else:
                    roles[role] = 1
                    
            for role, count in roles.items():
                print(f"  {role}: {count} users")
                
            print("\nAll users:")
            for user in users:
                print(f"  - {user.username} ({user.role}) - {user.full_name or 'No full name'}")
                
            # Check if there are any student users
            student_users = User.query.filter_by(role='student').all()
            if student_users:
                print(f"\n✅ Found {len(student_users)} student user(s):")
                for student in student_users:
                    print(f"  - Username: {student.username}")
                    print(f"    Full name: {student.full_name or 'Not set'}")
                    print(f"    Email: {student.email or 'Not set'}")
            else:
                print("\n❌ No student users found!")
                print("You need to create a student user to access the student dashboard.")
                
        except Exception as e:
            print(f"❌ Error checking users: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_users()