#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def reset_student_password():
    with app.app_context():
        try:
            # Find the student_user
            student = User.query.filter_by(username='student_user').first()
            if student:
                # Set a known password
                new_password = 'student123'
                student.password = generate_password_hash(new_password)
                db.session.commit()
                
                print("✅ Student password reset successfully!")
                print(f"Username: student_user")
                print(f"Password: {new_password}")
                print(f"Role: {student.role}")
                print(f"Full Name: {student.full_name}")
                print("\nYou can now log in with these credentials to access the student dashboard.")
            else:
                print("❌ student_user not found!")
                
                # Let's try student1 instead
                student1 = User.query.filter_by(username='student1').first()
                if student1:
                    new_password = 'student123'
                    student1.password = generate_password_hash(new_password)
                    db.session.commit()
                    
                    print("✅ student1 password reset successfully!")
                    print(f"Username: student1")
                    print(f"Password: {new_password}")
                    print(f"Role: {student1.role}")
                    print("\nYou can now log in with these credentials to access the student dashboard.")
                else:
                    print("❌ No student users found!")
                    
        except Exception as e:
            print(f"❌ Error resetting password: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reset_student_password()