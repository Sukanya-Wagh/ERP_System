from extension import db
from models import *
from app import app

def detailed_data_report():
    with app.app_context():
        print("=== DETAILED DATABASE REPORT ===\n")
        
        # Users table
        print("USERS (86 records):")
        users = User.query.limit(10).all()
        for user in users:
            print(f"  ID: {user.id}, Username: {user.username}, Role: {user.role}, Email: {user.email}")
        print()
        
        # Complaints
        print("COMPLAINTS (2 records):")
        complaints = Complaint.query.all()
        for complaint in complaints:
            print(f"  ID: {complaint.id}, Subject: {complaint.subject}, Status: {complaint.status}")
        print()
        
        # Workload
        print("WORKLOAD (4 records):")
        workloads = Workload.query.all()
        for workload in workloads:
            print(f"  ID: {workload.id}, Faculty: {workload.faculty_id}, Subject: {workload.subject}, Hours: {workload.hours}")
        print()
        
        # Reports
        print("REPORTS (5 records):")
        reports = Report.query.all()
        for report in reports:
            print(f"  ID: {report.id}, Type: {report.report_type}, Faculty: {report.faculty_id}")
        print()
        
        # Announcements
        print("ANNOUNCEMENTS (11 records):")
        announcements = Announcement.query.limit(5).all()
        for announcement in announcements:
            print(f"  ID: {announcement.id}, Title: {announcement.title[:50]}...")
        print()
        
        # Subjects
        print("SUBJECTS (9 records):")
        subjects = Subject.query.all()
        for subject in subjects:
            print(f"  ID: {subject.id}, Name: {subject.name}, Code: {subject.code}")
        print()
        
        # Leave Requests
        print("LEAVE REQUESTS (14 records):")
        leave_requests = LeaveRequest.query.limit(5).all()
        for leave in leave_requests:
            print(f"  ID: {leave.id}, Faculty: {leave.faculty_id}, Status: {leave.status}")
        print()
        
        # Test Marks
        print("TEST MARKS (6 records):")
        test_marks = TestMarks.query.all()
        for tm in test_marks:
            print(f"  ID: {tm.id}, Student: {tm.student_id}, Subject: {tm.subject_id}, Marks: {tm.marks}")
        print()
        
        # Summary
        print("=== SUMMARY ===")
        print(f"Total Users: {User.query.count()}")
        print(f"Total Complaints: {Complaint.query.count()}")
        print(f"Total Workload Records: {Workload.query.count()}")
        print(f"Total Reports: {Report.query.count()}")
        print(f"Total Announcements: {Announcement.query.count()}")
        print(f"Total Subjects: {Subject.query.count()}")
        print(f"Total Leave Requests: {LeaveRequest.query.count()}")
        print(f"Total Test Marks: {TestMarks.query.count()}")

if __name__ == "__main__":
    detailed_data_report()
