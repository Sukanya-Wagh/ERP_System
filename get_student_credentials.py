#!/usr/bin/env python3
"""
Get all student user credentials from the database
"""

from app import app
from models import User
from extension import db

def get_student_credentials():
    with app.app_context():
        print("=== STUDENT USER CREDENTIALS ===\n")
        
        # Get all student users
        students = User.query.filter_by(role='student', is_active=True).all()
        
        if not students:
            print("No student users found in database!")
            return
        
        print(f"Total Active Students: {len(students)}\n")
        
        for student in students:
            print(f"Student ID: {student.id}")
            print(f"Username: {student.username}")
            print(f"Full Name: {student.full_name or 'Not set'}")
            print(f"Email: {student.email or 'Not set'}")
            print(f"Roll Number: {student.roll_number or 'Not set'}")
            print(f"Section: {student.section or 'Not set'}")
            print(f"Date Joined: {student.date_joined}")
            print(f"Last Login: {student.last_login or 'Never logged in'}")
            print("-" * 50)
        
        print("\n=== LOGIN CREDENTIALS SUMMARY ===")
        print("Username Format: Usually roll number or student code")
        print("Password Format: Usually 'student123' or similar pattern")
        print("\nYou can try these common passwords:")
        print("- student123")
        print("- password")
        print("- 123456")
        print("- [rollnumber] (e.g., 2023001)")
        
        print(f"\n=== TESTING LOGIN ===")
        print("Test with these usernames on login page:")
        for student in students[:5]:  # Show first 5 students
            print(f"- Username: {student.username}")

if __name__ == "__main__":
    get_student_credentials()
