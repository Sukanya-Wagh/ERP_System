#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def reset_all_student_passwords():
    with app.app_context():
        try:
            # Find all student users
            students = User.query.filter_by(role='student').all()
            
            if not students:
                print("❌ No student users found!")
                return
            
            # Set password for all students
            new_password = 'student123'
            password_hash = generate_password_hash(new_password)
            
            updated_count = 0
            
            print("🔄 Resetting passwords for all student users...")
            print("=" * 60)
            
            for student in students:
                student.password = password_hash
                updated_count += 1
                print(f"✅ {student.username} - Password reset successfully")
            
            # Commit all changes
            db.session.commit()
            
            print("=" * 60)
            print(f"🎉 Successfully reset passwords for {updated_count} student users!")
            print(f"📝 Common Password: {new_password}")
            print("\n📋 Student Login Credentials:")
            print("Username: Any student username from the list")
            print("Password: student123")
            print("\n🔐 Example logins:")
            print("- Username: student_user, Password: student123")
            print("- Username: student1, Password: student123")
            print("- Username: patil01, Password: student123")
            print("- Username: shinde02, Password: student123")
            print("- And so on for all student users...")
            
        except Exception as e:
            print(f"❌ Error resetting passwords: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reset_all_student_passwords()