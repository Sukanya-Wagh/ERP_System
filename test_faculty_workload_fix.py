#!/usr/bin/env python3
"""
Test that faculty workload view shows correct data
"""

from app import app
from models import Workload, User
from extension import db

def test_faculty_workload_view():
    with app.app_context():
        print("=== TESTING FACULTY WORKLOAD VIEW FIX ===\n")
        
        # Test with different faculty users
        faculty_users = User.query.filter_by(role='faculty', is_active=True).all()
        
        for faculty in faculty_users:
            print(f"Testing faculty: {faculty.full_name or faculty.username} (ID: {faculty.id})")
            
            # Simulate the view_workload route logic
            my_workloads = Workload.query.filter_by(faculty_id=faculty.id).order_by(Workload.timestamp.desc()).all()
            
            total_lectures = 0
            total_practicals = 0
            
            for workload in my_workloads:
                if workload.workload_type.lower() == 'theory':
                    total_lectures += workload.hours
                elif workload.workload_type.lower() == 'practical':
                    total_practicals += workload.hours
            
            print(f"  Workload count: {len(my_workloads)}")
            print(f"  Total hours: {sum(w.hours for w in my_workloads)}")
            print(f"  Lecture hours: {total_lectures}")
            print(f"  Practical hours: {total_practicals}")
            
            if my_workloads:
                print("  Assignments:")
                for w in my_workloads:
                    assigner = User.query.get(w.assigned_by) if w.assigned_by else None
                    print(f"    • {w.subject} ({w.hours}hrs, {w.workload_type}) - Assigned by: {assigner.full_name or assigner.username if assigner else 'N/A'}")
            else:
                print("  No assignments found")
            
            print()
        
        # Specifically test A.A.Piske who has CSS assignment
        piske = User.query.filter_by(username='A.A.Piske').first()
        if piske:
            print("=== SPECIFIC TEST: A.A.Piske (CSS Assignment) ===")
            piske_workloads = Workload.query.filter_by(faculty_id=piske.id).all()
            
            for w in piske_workloads:
                print(f"Subject: {w.subject}")
                print(f"Hours: {w.hours}")
                print(f"Type: {w.workload_type}")
                print(f"Assigned by: {User.query.get(w.assigned_by).full_name if w.assigned_by else 'N/A'}")
                print(f"Date: {w.timestamp}")
                print("---")
            
            if piske_workloads:
                print("✅ CSS assignment found and should display on faculty dashboard!")
            else:
                print("❌ No assignments found for A.A.Piske")

if __name__ == "__main__":
    test_faculty_workload_view()
