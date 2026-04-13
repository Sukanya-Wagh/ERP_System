print("=== DEPARTMENTAL ERP SYSTEM - DATABASE STRUCTURE ===\n")

print("🗄️  DATABASE TYPE: SQLite")
print("📁 DATABASE FILE: faculty_workload.db")
print("🔧 ORM: Flask-SQLAlchemy\n")

print("📊 COMPLETE TABLE STRUCTURE:\n")

tables_info = [
    {
        "name": "User",
        "description": "मुख्य वापरकर्ता टेबल - सर्व भूमिका वापरकर्ते",
        "columns": [
            "id (Integer, Primary Key)",
            "username (String 150, Unique, Not Null)",
            "password_hash (String 256)",
            "role (String 20, Not Null) - hod, cc, faculty, student",
            "email (String 120, Unique)",
            "phone (String 15)",
            "full_name (String 200)",
            "department (String 100)",
            "profile_picture (String 200)",
            "date_joined (DateTime)",
            "last_login (DateTime)",
            "is_active (Boolean, Default True)",
            "roll_number (String 20) - विद्यार्थ्यांसाठी",
            "section (String 10) - विद्यार्थ्यांसाठी"
        ]
    },
    {
        "name": "Complaint",
        "description": "तक्रार व्यवस्थापन प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "title (String 200, Not Null)",
            "description (Text, Not Null)",
            "category (String 50, Not Null)",
            "priority (String 20, Not Null)",
            "submitted_by (Integer, Foreign Key → User)",
            "status (String 20, Default 'Pending')",
            "comments (Text)",
            "resolved_by (Integer, Foreign Key → User)",
            "timestamp (DateTime)",
            "resolved_at (DateTime)"
        ]
    },
    {
        "name": "Workload",
        "description": "फॅकल्टी कामाचे वेळापत्रक आणि वर्कलोड",
        "columns": [
            "id (Integer, Primary Key)",
            "faculty_id (Integer, Foreign Key → User)",
            "subject (String 150)",
            "subject_id (Integer, Foreign Key → Subject)",
            "workload_type (String 50, Default 'Theory')",
            "semester (String 20, Default 'Current')",
            "hours (Integer, Not Null)",
            "assigned_by (Integer, Foreign Key → User)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "Marks",
        "description": "विद्यार्थी गुण नोंदणी प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "student_id (Integer, Foreign Key → User)",
            "cc_id (Integer, Foreign Key → User)",
            "subject (String 100, Not Null)",
            "marks_obtained (Float, Not Null)",
            "total_marks (Float, Not Null)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "Notification",
        "description": "सूचना प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "user_id (Integer, Foreign Key → User)",
            "title (String 200, Not Null)",
            "message (Text, Not Null)",
            "is_read (Boolean, Default False)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "Attendance",
        "description": "फॅकल्टी उपस्थिती नोंदणी",
        "columns": [
            "id (Integer, Primary Key)",
            "user_id (Integer, Foreign Key → User)",
            "date (Date, Not Null)",
            "check_in (DateTime)",
            "check_out (DateTime)",
            "status (String 20, Default 'Present')",
            "hours_worked (Float, Default 0.0)",
            "notes (Text)"
        ]
    },
    {
        "name": "Schedule",
        "description": "फॅकल्टी वेळापत्रक",
        "columns": [
            "id (Integer, Primary Key)",
            "faculty_id (Integer, Foreign Key → User)",
            "subject (String 150, Not Null)",
            "day_of_week (String 10, Not Null)",
            "start_time (Time, Not Null)",
            "end_time (Time, Not Null)",
            "room_number (String 50)",
            "semester (String 20)",
            "academic_year (String 20)"
        ]
    },
    {
        "name": "Report",
        "description": "रिपोर्ट व्यवस्थापन प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "title (String 200, Not Null)",
            "report_type (String 50, Not Null)",
            "generated_by (Integer, Foreign Key → User)",
            "file_path (String 300)",
            "parameters (Text - JSON)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "SystemSettings",
        "description": "सिस्टम सेटिंग्ज व्यवस्थापन",
        "columns": [
            "id (Integer, Primary Key)",
            "setting_key (String 100, Unique, Not Null)",
            "setting_value (Text)",
            "description (Text)",
            "updated_by (Integer, Foreign Key → User)",
            "updated_at (DateTime)"
        ]
    },
    {
        "name": "AuditLog",
        "description": "ऑडिट लॉग - सर्व क्रियांचा इतिहास",
        "columns": [
            "id (Integer, Primary Key)",
            "user_id (Integer, Foreign Key → User)",
            "action (String 100, Not Null)",
            "table_name (String 50)",
            "record_id (Integer)",
            "old_values (Text - JSON)",
            "new_values (Text - JSON)",
            "timestamp (DateTime)",
            "ip_address (String 45)"
        ]
    },
    {
        "name": "Announcement",
        "description": "जाहिरात प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "title (String 200, Not Null)",
            "content (Text, Not Null)",
            "created_by (Integer, Foreign Key → User)",
            "target_role (String 20, Not Null)",
            "priority (String 10, Default 'normal')",
            "is_active (Boolean, Default True)",
            "expires_at (DateTime)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "Subject",
        "description": "विषय माहिती व्यवस्थापन",
        "columns": [
            "id (Integer, Primary Key)",
            "name (String 150, Not Null)",
            "code (String 20, Unique, Not Null)",
            "department (String 100)",
            "semester (String 20)",
            "credits (Integer, Default 3)",
            "description (Text)",
            "is_active (Boolean, Default True)",
            "created_at (DateTime)"
        ]
    },
    {
        "name": "FacultySubject",
        "description": "फॅकल्टी-विषय असाइनमेंट",
        "columns": [
            "id (Integer, Primary Key)",
            "faculty_id (Integer, Foreign Key → User)",
            "subject_id (Integer, Foreign Key → Subject)",
            "assigned_by (Integer, Foreign Key → User)",
            "academic_year (String 20)",
            "semester (String 20)",
            "class_section (String 10)",
            "assigned_at (DateTime)"
        ]
    },
    {
        "name": "TestMarks",
        "description": "विद्यार्थी चाचणी गुण नोंदणी",
        "columns": [
            "id (Integer, Primary Key)",
            "student_id (Integer, Foreign Key → User)",
            "subject_id (Integer, Foreign Key → Subject)",
            "faculty_id (Integer, Foreign Key → User)",
            "test_number (Integer, Not Null)",
            "marks_obtained (Float, Not Null)",
            "total_marks (Float, Not Null)",
            "test_date (Date)",
            "remarks (Text)",
            "proof_file_path (String 300)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "LabPerformance",
        "description": "प्रयोगशाळा कामगिरी मूल्यांकन",
        "columns": [
            "id (Integer, Primary Key)",
            "student_id (Integer, Foreign Key → User)",
            "subject_id (Integer, Foreign Key → Subject)",
            "faculty_id (Integer, Foreign Key → User)",
            "lab_session (String 100, Not Null)",
            "performance_score (Float, Not Null)",
            "attendance (String 10, Default 'Present')",
            "practical_marks (Float)",
            "viva_marks (Float)",
            "assignment_marks (Float)",
            "total_marks (Float)",
            "comments (Text)",
            "lab_date (Date, Not Null)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "StudyMaterial",
        "description": "अभ्यास साहित्य अपलोड प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "title (String 200, Not Null)",
            "description (Text)",
            "subject_id (Integer, Foreign Key → Subject)",
            "uploaded_by (Integer, Foreign Key → User)",
            "file_path (String 300, Not Null)",
            "file_name (String 200, Not Null)",
            "file_size (Integer)",
            "file_type (String 50)",
            "download_count (Integer, Default 0)",
            "is_active (Boolean, Default True)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "StudentFeedback",
        "description": "विद्यार्थी फीडबॅक प्रणाली (१० प्रश्न)",
        "columns": [
            "id (Integer, Primary Key)",
            "student_id (Integer, Foreign Key → User)",
            "faculty_id (Integer, Foreign Key → User)",
            "subject_id (Integer, Foreign Key → Subject)",
            "teaching_clarity (Integer, 1-5 rating)",
            "subject_knowledge (Integer, 1-5 rating)",
            "communication_skills (Integer, 1-5 rating)",
            "punctuality (Integer, 1-5 rating)",
            "assignment_feedback (Integer, 1-5 rating)",
            "doubt_resolution (Integer, 1-5 rating)",
            "course_completion (Integer, 1-5 rating)",
            "practical_approach (Integer, 1-5 rating)",
            "student_interaction (Integer, 1-5 rating)",
            "overall_satisfaction (Integer, 1-5 rating)",
            "additional_comments (Text)",
            "suggestions (Text)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "Assignment",
        "description": "असाइनमेंट व्यवस्थापन प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "title (String 200, Not Null)",
            "description (Text, Not Null)",
            "subject_id (Integer, Foreign Key → Subject)",
            "faculty_id (Integer, Foreign Key → User)",
            "due_date (DateTime, Not Null)",
            "max_marks (Float, Default 100)",
            "file_path (String 300)",
            "is_active (Boolean, Default True)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "AssignmentSubmission",
        "description": "असाइनमेंट सबमिशन ट्रॅकिंग",
        "columns": [
            "id (Integer, Primary Key)",
            "assignment_id (Integer, Foreign Key → Assignment)",
            "student_id (Integer, Foreign Key → User)",
            "file_path (String 300, Not Null)",
            "submission_text (Text)",
            "marks_obtained (Float)",
            "feedback (Text)",
            "status (String 20, Default 'Submitted')",
            "submitted_at (DateTime)",
            "graded_at (DateTime)"
        ]
    },
    {
        "name": "ExamTimetable",
        "description": "परीक्षा वेळापत्रक व्यवस्थापन",
        "columns": [
            "id (Integer, Primary Key)",
            "subject_id (Integer, Foreign Key → Subject)",
            "exam_type (String 50, Not Null)",
            "exam_date (DateTime, Not Null)",
            "duration (Integer - minutes)",
            "room_number (String 50)",
            "max_marks (Float, Default 100)",
            "instructions (Text)",
            "created_by (Integer, Foreign Key → User)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "StudentAttendance",
        "description": "विद्यार्थी उपस्थिती नोंदणी",
        "columns": [
            "id (Integer, Primary Key)",
            "student_id (Integer, Foreign Key → User)",
            "subject_id (Integer, Foreign Key → Subject)",
            "faculty_id (Integer, Foreign Key → User)",
            "date (Date, Not Null)",
            "status (String 10, Default 'Present')",
            "lecture_type (String 20, Default 'Theory')",
            "remarks (Text)",
            "marked_by (Integer, Foreign Key → User)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "LeaveRequest",
        "description": "रजा विनंती प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "user_id (Integer, Foreign Key → User)",
            "approver_id (Integer, Foreign Key → User)",
            "leave_type (String 50, Not Null)",
            "start_date (Date, Not Null)",
            "end_date (Date, Not Null)",
            "reason (Text, Not Null)",
            "status (String 20, Default 'Pending')",
            "comments (Text)",
            "timestamp (DateTime)"
        ]
    },
    {
        "name": "ModelAnswer",
        "description": "मॉडेल उत्तरे अपलोड प्रणाली",
        "columns": [
            "id (Integer, Primary Key)",
            "subject_code (String 10, Not Null)",
            "subject_name (String 100, Not Null)",
            "title (String 200, Not Null)",
            "description (Text)",
            "file_path (String 300, Not Null)",
            "file_type (String 20)",
            "uploaded_by (Integer, Foreign Key → User)",
            "semester (String 20)",
            "academic_year (String 20)",
            "is_active (Boolean, Default True)",
            "download_count (Integer, Default 0)",
            "timestamp (DateTime)"
        ]
    }
]

for i, table in enumerate(tables_info, 1):
    print(f"🗂️  TABLE {i}: {table['name'].upper()}")
    print(f"📝 वर्णन: {table['description']}")
    print("📋 कॉलम्स:")
    for col in table['columns']:
        print(f"   • {col}")
    print("\n" + "="*80 + "\n")

print("🔗 USER ROLES (वापरकर्ता भूमिका):")
print("   • HOD - Head of Department (विभाग प्रमुख)")
print("   • CC - Class Coordinator (वर्ग समन्वयक)")
print("   • Faculty - Faculty/Teacher (प्राध्यापक)")
print("   • Student - Student (विद्यार्थी)")

print("\n📊 TOTAL TABLES: 22")
print("🔗 TOTAL FOREIGN KEY RELATIONSHIPS: 50+")
print("📈 DATABASE FEATURES:")
print("   • Complete CRUD Operations")
print("   • Role-based Access Control")
print("   • Audit Trail System")
print("   • File Upload Management")
print("   • Notification System")
print("   • Reporting & Analytics")
print("   • Leave Management")
print("   • Feedback System")
