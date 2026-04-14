#!/usr/bin/env python3
"""
Fix workload assignment issues
"""

from app import app
from models import Workload, User, Subject
from extension import db

def fix_workload_issues():
    with app.app_context():
        print("=== FIXING WORKLOAD ASSIGNMENT ISSUES ===\n")
        
        # Get HOD user for proper assignment
        hod = User.query.filter_by(role='hod', is_active=True).first()
        if not hod:
            print("ERROR: No active HOD found!")
            return
        
        print(f"Using HOD: {hod.full_name or hod.username} (ID: {hod.id})")
        
        # Get subjects to assign
        subjects = Subject.query.filter_by(is_active=True).all()
        if not subjects:
            print("ERROR: No subjects found in database!")
            return
        
        print(f"Available subjects: {[s.name for s in subjects]}")
        
        # Fix problematic workload assignments
        problematic_workloads = Workload.query.filter(
            (Workload.subject.is_(None)) | 
            (Workload.subject == '') |
            (Workload.assigned_by.is_(None))
        ).all()
        
        print(f"\nFound {len(problematic_workloads)} problematic assignments:")
        
        for w in problematic_workloads:
            print(f"\nFixing assignment ID: {w.id}")
            print(f"  Faculty: {w.faculty.full_name or w.faculty.username}")
            print(f"  Current subject: '{w.subject}' (ID: {w.subject_id})")
            print(f"  Current assigner: {w.assigned_by}")
            
            # Assign proper subject name if subject_id exists
            if w.subject_id:
                subject = Subject.query.get(w.subject_id)
                if subject:
                    w.subject = subject.name
                    print(f"  Updated subject name to: {subject.name}")
            
            # Assign proper HOD if missing
            if not w.assigned_by:
                w.assigned_by = hod.id
                print(f"  Updated assigner to HOD: {hod.full_name or hod.username}")
            
            # If still no subject, assign one from available subjects
            if not w.subject or w.subject.strip() == '':
                # Use first available subject
                w.subject = subjects[0].name
                w.subject_id = subjects[0].id
                print(f"  Assigned default subject: {subjects[0].name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n=== SUCCESS: All workload issues fixed! ===")
        except Exception as e:
            print(f"ERROR: Failed to save changes - {e}")
            db.session.rollback()
            return
        
        # Verify the fixes
        print("\n=== VERIFICATION ===")
        all_workloads = Workload.query.all()
        for w in all_workloads:
            faculty = User.query.get(w.faculty_id)
            assigner = User.query.get(w.assigned_by) if w.assigned_by else None
            
            status = "OK"
            if not w.subject or w.subject.strip() == '':
                status = "MISSING SUBJECT"
            elif not w.assigned_by:
                status = "MISSING ASSIGNER"
            
            print(f"ID {w.id}: {faculty.full_name or faculty.username} - '{w.subject}' - {w.hours}hrs - {status}")

if __name__ == "__main__":
    fix_workload_issues()
