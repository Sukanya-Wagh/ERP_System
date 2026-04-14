"""
Test script to verify workload display for faculty dashboard
"""

from app import app
from models import User, Workload, Subject, LeaveRequest, Notification, TestMarks
from extension import db
from werkzeug.security import generate_password_hash

def create_test_data():
    """Create test workload data for faculty"""
    with app.app_context():
        print("Creating test workload data...")
        
        # Create test faculty if not exists
        faculty = User.query.filter_by(username='testfaculty').first()
        if not faculty:
            faculty = User(
                username='testfaculty',
                full_name='Test Faculty Member',
                role='faculty',
                email='faculty@test.com',
                department='Information Technology'
            )
            faculty.set_password('testpass')
            db.session.add(faculty)
            db.session.commit()
            print("Created test faculty user")
        
        # Create test subjects
        subjects_data = [
            ('OOP', 'Object Oriented Programming'),
            ('DSU', 'Data Structures Using Python'),
            ('DTM', 'Database Management Systems')
        ]
        
        subjects = []
        for code, name in subjects_data:
            subject = Subject.query.filter_by(code=code).first()
            if not subject:
                subject = Subject(
                    code=code,
                    name=name,
                    department='Information Technology',
                    semester='Current',
                    credits=4
                )
                db.session.add(subject)
                db.session.commit()
            subjects.append(subject)
        
        # Create test workload assignments
        workload_data = [
            (faculty.id, subjects[0].id, 'Theory', 6),
            (faculty.id, subjects[1].id, 'Theory', 4),
            (faculty.id, subjects[2].id, 'Practical', 4)
        ]
        
        # Clear existing workload for test faculty
        Workload.query.filter_by(faculty_id=faculty.id).delete()
        db.session.commit()
        
        # Add new workload assignments
        for faculty_id, subject_id, workload_type, hours in workload_data:
            workload = Workload(
                faculty_id=faculty_id,
                subject_id=subject_id,
                workload_type=workload_type,
                hours=hours,
                semester='Current'
            )
            db.session.add(workload)
        
        db.session.commit()
        print("Created test workload assignments")
        
        return faculty

def test_workload_display():
    """Test workload display functionality"""
    with app.app_context():
        print("\n=== Testing Workload Display ===")
        
        faculty = User.query.filter_by(username='testfaculty').first()
        if not faculty:
            print("Test faculty not found!")
            return
        
        print(f"Faculty: {faculty.full_name}")
        print(f"Faculty ID: {faculty.id}")
        
        # Get workload data (same as in faculty_dashboard function)
        my_workloads = Workload.query.filter_by(faculty_id=faculty.id).all()
        
        print(f"\nWorkload Count: {len(my_workloads)}")
        
        # Calculate statistics
        workload_count = len(my_workloads)
        total_lectures = 0
        total_practicals = 0
        
        print("\nWorkload Details:")
        for i, workload in enumerate(my_workloads, 1):
            subject = Subject.query.get(workload.subject_id)
            print(f"  {i}. {subject.name if subject else 'Unknown'} - {workload.workload_type} ({workload.hours} hrs)")
            
            if workload.workload_type.lower() == 'theory':
                total_lectures += workload.hours
            elif workload.workload_type.lower() == 'practical':
                total_practicals += workload.hours
        
        print(f"\nStatistics:")
        print(f"  Total Workload Assignments: {workload_count}")
        print(f"  Total Lecture Hours: {total_lectures}")
        print(f"  Total Practical Hours: {total_practicals}")
        print(f"  Total Hours: {total_lectures + total_practicals}")
        
        # Test dashboard data
        print(f"\n=== Dashboard Data Test ===")
        print(f"workload_count: {workload_count}")
        print(f"total_lectures: {total_lectures}")
        print(f"total_practicals: {total_practicals}")
        
        # Test other dashboard stats
        leave_requests = LeaveRequest.query.filter_by(user_id=faculty.id).count()
        unread_notifications = Notification.query.filter_by(user_id=faculty.id, is_read=False).count()
        marks_entered = TestMarks.query.filter_by(faculty_id=faculty.id).count()
        
        print(f"\nOther Dashboard Stats:")
        print(f"leave_requests: {leave_requests}")
        print(f"notifications: {unread_notifications}")
        print(f"marks_entered: {marks_entered}")
        
        print("\n=== Test Results ===")
        if workload_count > 0:
            print("SUCCESS: Faculty workload data is available!")
            print("The faculty dashboard should now show:")
            print(f"  - {workload_count} workload assignments")
            print(f"  - {total_lectures} lecture hours")
            print(f"  - {total_practicals} practical hours")
        else:
            print("WARNING: No workload data found for faculty")
        
        print("\n=== Login Credentials for Testing ===")
        print("Username: testfaculty")
        print("Password: testpass")
        print("Role: faculty")

if __name__ == "__main__":
    print("=== Faculty Workload Display Test ===")
    
    with app.app_context():
        # Create test data
        faculty = create_test_data()
        
        # Test workload display
        test_workload_display()
        
    print("\n=== Next Steps ===")
    print("1. Run the Flask application: python app.py")
    print("2. Login with test faculty credentials")
    print("3. Check the 'My Workload' section on the dashboard")
    print("4. Verify that workload data is displayed correctly")
