#!/usr/bin/env python3
"""
Test the complete workload assignment workflow
"""

from app import app
from models import Workload, User
from extension import db

def test_workload_workflow():
    with app.app_context():
        print("=== WORKLOAD ASSIGNMENT WORKFLOW TEST ===\n")
        
        # 1. Check HOD users
        hod_users = User.query.filter_by(role='hod', is_active=True).all()
        print(f"Active HOD users: {len(hod_users)}")
        for hod in hod_users:
            print(f"  {hod.full_name or hod.username} (ID: {hod.id})")
        
        # 2. Check faculty users
        faculty_users = User.query.filter_by(role='faculty', is_active=True).all()
        print(f"\nActive faculty users: {len(faculty_users)}")
        for faculty in faculty_users:
            workload_count = Workload.query.filter_by(faculty_id=faculty.id).count()
            print(f"  {faculty.full_name or faculty.username} (ID: {faculty.id}) - {workload_count} assignments")
        
        # 3. Check workload assignments with missing data
        print("\n=== WORKLOAD ASSIGNMENTS ANALYSIS ===")
        workloads = Workload.query.all()
        
        for i, w in enumerate(workloads, 1):
            faculty = User.query.get(w.faculty_id)
            assigner = User.query.get(w.assigned_by) if w.assigned_by else None
            
            print(f"\nAssignment {i}:")
            print(f"  Faculty: {faculty.full_name or faculty.username}")
            print(f"  Subject: '{w.subject}' (ID: {w.subject_id})")
            print(f"  Hours: {w.hours}")
            print(f"  Type: {w.workload_type}")
            print(f"  Assigned by: {assigner.full_name or assigner.username if assigner else 'NOT ASSIGNED'}")
            print(f"  Date: {w.timestamp}")
            
            # Check for issues
            issues = []
            if not w.subject or w.subject.strip() == '':
                issues.append("Missing subject name")
            if not w.assigned_by:
                issues.append("Missing assigner (HOD)")
            if w.hours <= 0:
                issues.append("Invalid hours")
                
            if issues:
                print(f"  ISSUES: {', '.join(issues)}")
            else:
                print(f"  STATUS: OK")
        
        # 4. Test faculty dashboard data preparation
        print("\n=== FACULTY DASHBOARD DATA TEST ===")
        test_faculty = User.query.filter_by(username='testfaculty').first()
        if test_faculty:
            print(f"Testing with faculty: {test_faculty.full_name or test_faculty.username}")
            
            # Simulate faculty_dashboard workload data calculation
            my_workloads = Workload.query.filter_by(faculty_id=test_faculty.id).all()
            workload_count = len(my_workloads)
            total_lectures = 0
            total_practicals = 0
            
            for workload in my_workloads:
                if workload.workload_type.lower() == 'theory':
                    total_lectures += workload.hours
                elif workload.workload_type.lower() == 'practical':
                    total_practicals += workload.hours
            
            print(f"  Workload count: {workload_count}")
            print(f"  Total lecture hours: {total_lectures}")
            print(f"  Total practical hours: {total_practicals}")
            print(f"  Total hours: {total_lectures + total_practicals}")
            
            if workload_count > 0:
                print("  STATUS: Faculty should see workload on dashboard")
            else:
                print("  STATUS: No workload to display")
        else:
            print("Test faculty not found")

if __name__ == "__main__":
    test_workload_workflow()
