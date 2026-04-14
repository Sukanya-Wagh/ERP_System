#!/usr/bin/env python3
"""
Check workload assignments in the database
"""

from app import app
from models import Workload, User
from extension import db

def check_workload_data():
    with app.app_context():
        print("=== WORKLOAD ASSIGNMENT CHECK ===\n")
        
        # Check total workload assignments
        workloads = Workload.query.all()
        print(f"Total workload assignments: {len(workloads)}")
        
        if workloads:
            print("\nRecent workload assignments:")
            for w in workloads[:5]:
                faculty = User.query.get(w.faculty_id)
                assigner = User.query.get(w.assigned_by) if w.assigned_by else None
                print(f"ID: {w.id}")
                print(f"  Faculty: {faculty.full_name or faculty.username} (ID: {w.faculty_id})")
                print(f"  Subject: {w.subject}")
                print(f"  Hours: {w.hours}")
                print(f"  Type: {w.workload_type}")
                print(f"  Assigned by: {assigner.full_name or assigner.username if assigner else 'N/A'}")
                print(f"  Date: {w.timestamp}")
                print()
        else:
            print("No workload assignments found in database!")
        
        # Check faculty users
        faculty_users = User.query.filter_by(role='faculty', is_active=True).all()
        print(f"\nActive faculty users: {len(faculty_users)}")
        for f in faculty_users:
            workload_count = Workload.query.filter_by(faculty_id=f.id).count()
            print(f"  {f.full_name or f.username}: {workload_count} assignments")

if __name__ == "__main__":
    check_workload_data()
