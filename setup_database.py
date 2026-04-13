#!/usr/bin/env python3
"""
Database Setup Script for Faculty Workload Management System
This script creates all tables and populates them with sample data
"""

from app import app, db
from models import (User, Subject, FacultySubject, Announcement, TestMarks, 
                   LabPerformance, StudyMaterial, StudentFeedback, Complaint)
from datetime import datetime, date
import os

def create_sample_data():
    """Create sample users, subjects, and other data"""
    
    # Create HOD user (A.S.Bhatlawand)
    hod = User(
        username='hod_user',
        full_name='A.S.Bhatlawand',
        email='hod@college.edu',
        role='hod',
        department='Information Technology',
        is_active=True
    )
    hod.set_password('hod123')
    
    # Create CC user
    cc = User(
        username='cc_user',
        full_name='Dr. Priya Sharma',
        email='cc@college.edu',
        role='cc',
        department='Information Technology',
        is_active=True
    )
    cc.set_password('cc123')
    
    # Create Faculty users
    faculty1 = User(
        username='faculty1',
        full_name='Prof. Rajesh Kumar',
        email='rajesh@college.edu',
        role='faculty',
        department='Information Technology',
        is_active=True
    )
    faculty1.set_password('faculty123')
    
    faculty2 = User(
        username='faculty2',
        full_name='Dr. Sneha Patel',
        email='sneha@college.edu',
        role='faculty',
        department='Information Technology',
        is_active=True
    )
    faculty2.set_password('faculty123')
    
    faculty3 = User(
        username='faculty3',
        full_name='Prof. Amit Singh',
        email='amit@college.edu',
        role='faculty',
        department='Information Technology',
        is_active=True
    )
    faculty3.set_password('faculty123')
    
    # Create Student users
    students = []
    student_names = [
        'Aditi Patil', 'Rohit Sharma', 'Priya Gupta', 'Arjun Reddy', 'Kavya Nair',
        'Vikram Joshi', 'Ananya Das', 'Karan Mehta', 'Riya Agarwal', 'Siddharth Rao'
    ]
    
    for i, name in enumerate(student_names, 1):
        student = User(
            username=f'student{i}',
            full_name=name,
            email=f'student{i}@college.edu',
            role='student',
            department='Information Technology',
            is_active=True
        )
        student.set_password('student123')
        students.append(student)
    
    # Add all users to session
    db.session.add_all([hod, cc, faculty1, faculty2, faculty3] + students)
    db.session.commit()
    
    # Create Subjects with course codes
    subjects = [
        Subject(name='Data Structures and Algorithms', code='CS201', department='IT', semester='3', credits=4),
        Subject(name='Database Management Systems', code='CS202', department='IT', semester='3', credits=4),
        Subject(name='Computer Networks', code='CS301', department='IT', semester='5', credits=3),
        Subject(name='Software Engineering', code='CS302', department='IT', semester='5', credits=4),
        Subject(name='Web Technologies', code='CS303', department='IT', semester='5', credits=3),
        Subject(name='Machine Learning', code='CS401', department='IT', semester='7', credits=4),
        Subject(name='Artificial Intelligence', code='CS402', department='IT', semester='7', credits=4),
        Subject(name='Mobile Application Development', code='CS403', department='IT', semester='7', credits=3),
    ]
    
    db.session.add_all(subjects)
    db.session.commit()
    
    # Assign subjects to faculty
    faculty_assignments = [
        FacultySubject(faculty_id=faculty1.id, subject_id=subjects[0].id, assigned_by=hod.id, 
                      academic_year='2024-25', semester='3', class_section='A'),
        FacultySubject(faculty_id=faculty1.id, subject_id=subjects[1].id, assigned_by=hod.id,
                      academic_year='2024-25', semester='3', class_section='A'),
        FacultySubject(faculty_id=faculty2.id, subject_id=subjects[2].id, assigned_by=hod.id,
                      academic_year='2024-25', semester='5', class_section='A'),
        FacultySubject(faculty_id=faculty2.id, subject_id=subjects[3].id, assigned_by=hod.id,
                      academic_year='2024-25', semester='5', class_section='A'),
        FacultySubject(faculty_id=faculty3.id, subject_id=subjects[4].id, assigned_by=hod.id,
                      academic_year='2024-25', semester='5', class_section='A'),
        FacultySubject(faculty_id=faculty3.id, subject_id=subjects[5].id, assigned_by=hod.id,
                      academic_year='2024-25', semester='7', class_section='A'),
    ]
    
    db.session.add_all(faculty_assignments)
    db.session.commit()
    
    # Create sample announcements
    hod_announcement = Announcement(
        title='Welcome to New Academic Year 2024-25',
        content='Dear Faculty, Welcome to the new academic year. Please ensure all course materials are updated and ready for the semester.',
        created_by=hod.id,
        target_role='faculty',
        priority='high'
    )
    
    cc_announcement = Announcement(
        title='Class Schedule Update',
        content='Dear Students, Please note that the class schedule for this week has been updated. Check your timetable for changes.',
        created_by=cc.id,
        target_role='student',
        priority='normal'
    )
    
    db.session.add_all([hod_announcement, cc_announcement])
    db.session.commit()
    
    # Create sample test marks for students
    for i, student in enumerate(students[:5]):  # First 5 students
        for j, subject in enumerate(subjects[:3]):  # First 3 subjects
            for test_num in range(1, 4):  # 3 tests
                marks = TestMarks(
                    student_id=student.id,
                    subject_id=subject.id,
                    faculty_id=faculty1.id if j < 2 else faculty2.id,
                    test_number=test_num,
                    marks_obtained=75 + (i * 2) + (j * 3) + (test_num * 2),
                    total_marks=100,
                    test_date=date(2024, 8, 15 + test_num * 7),
                    remarks='Good performance' if (75 + (i * 2) + (j * 3) + (test_num * 2)) > 80 else 'Needs improvement'
                )
                db.session.add(marks)
    
    # Create sample lab performance records
    for i, student in enumerate(students[:5]):
        for j, subject in enumerate(subjects[:2]):  # First 2 subjects with labs
            lab_perf = LabPerformance(
                student_id=student.id,
                subject_id=subject.id,
                faculty_id=faculty1.id,
                lab_session=f'Lab Session {j+1}',
                performance_score=8.0 + (i * 0.2),
                attendance='Present',
                practical_marks=18 + i,
                viva_marks=8 + i,
                assignment_marks=9 + i,
                total_marks=35 + (i * 3),
                comments='Excellent practical skills' if i < 3 else 'Good understanding',
                lab_date=date(2024, 8, 20 + j * 7)
            )
            db.session.add(lab_perf)
    
    # Create sample student feedback
    for i, student in enumerate(students[:3]):
        feedback = StudentFeedback(
            student_id=student.id,
            faculty_id=faculty1.id,
            subject_id=subjects[0].id,
            teaching_clarity=4 + (i % 2),
            subject_knowledge=5,
            communication_skills=4,
            punctuality=5,
            assignment_feedback=4,
            doubt_resolution=4 + (i % 2),
            course_completion=4,
            practical_approach=4,
            student_interaction=4 + (i % 2),
            overall_satisfaction=4,
            additional_comments='Great teaching style and very helpful',
            suggestions='More practical examples would be helpful'
        )
        db.session.add(feedback)
    
    # Create sample complaints
    complaint1 = Complaint(
        student_id=students[0].id,
        content='The lab equipment in Room 101 is not working properly. Please fix it.',
        status='Pending'
    )
    
    complaint2 = Complaint(
        student_id=students[1].id,
        content='Request for additional study materials for Database Management Systems.',
        status='Pending'
    )
    
    db.session.add_all([complaint1, complaint2])
    db.session.commit()
    
    print("✅ Sample data created successfully!")
    print("\n📋 Login Credentials:")
    print("HOD: username='hod_user', password='hod123'")
    print("CC: username='cc_user', password='cc123'")
    print("Faculty: username='faculty1', password='faculty123'")
    print("Student: username='student1', password='student123'")


def setup_database():
    """Initialize database and create sample data"""
    
    print("🔄 Setting up Faculty Workload Management System Database...")
    
    # Create upload directories
    upload_dirs = [
        'static/uploads',
        'static/uploads/profiles',
        'static/uploads/study_materials',
        'static/exports'
    ]
    
    for directory in upload_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create all database tables
    with app.app_context():
        db.drop_all()  # Remove existing tables
        db.create_all()  # Create new tables
        print("🗄️ Database tables created successfully!")
        
        # Create sample data
        create_sample_data()
    
    print("\n🎉 Database setup completed successfully!")
    print("🚀 You can now run the application with: python app.py")


if __name__ == '__main__':
    setup_database()
