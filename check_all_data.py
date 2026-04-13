from extension import db
from models import *
from app import app

def check_all_data():
    with app.app_context():
        # Get all table names
        tables = [User, Complaint, Workload, Marks, Notification, Attendance, 
                 Schedule, Report, SystemSettings, AuditLog, Announcement, Subject,
                 FacultySubject, TestMarks, LabPerformance, StudyMaterial, StudentFeedback,
                 Assignment, AssignmentSubmission, ExamTimetable, StudentAttendance, LeaveRequest, ModelAnswer]
        
        print("=== DATABASE TABLES AND DATA ===\n")
        
        for table in tables:
            table_name = table.__name__
            count = table.query.count()
            print(f"{table_name}: {count} records")
            
            if count > 0 and count <= 5:  # Show first 5 records if not too many
                records = table.query.limit(5).all()
                for record in records:
                    print(f"  - {record}")
                print()
            elif count > 5:
                print(f"  (showing first 3 of {count} records)")
                records = table.query.limit(3).all()
                for record in records:
                    print(f"  - {record}")
                print()

if __name__ == "__main__":
    check_all_data()
