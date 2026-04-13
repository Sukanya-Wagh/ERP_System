from extension import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False)  # hod, cc, faculty, student
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(15))
    full_name = db.Column(db.String(200))
    department = db.Column(db.String(100))
    profile_picture = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    roll_number = db.Column(db.String(20))  # For students
    section = db.Column(db.String(10))     # For students

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Under Investigation, Resolved, Rejected
    comments = db.Column(db.Text)  # Admin comments
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who resolved
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    submitter = db.relationship('User', foreign_keys=[submitted_by], backref='submitted_complaints')
    resolver = db.relationship('User', foreign_keys=[resolved_by])


class Workload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(150))          # plain subject name
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    workload_type = db.Column(db.String(50), default='Theory')
    semester = db.Column(db.String(20), default='Current')
    hours = db.Column(db.Integer, nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    faculty = db.relationship('User', foreign_keys=[faculty_id])
    hod = db.relationship('User', foreign_keys=[assigned_by])
    subject_rel = db.relationship('Subject', foreign_keys=[subject_id])


class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cc_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Who sent marks (CC)
    subject = db.Column(db.String(100), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', foreign_keys=[student_id])
    cc = db.relationship('User', foreign_keys=[cc_id])


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='notifications')


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, Late, Half-day
    hours_worked = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    
    user = db.relationship('User', backref='user_attendance_records')


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room_number = db.Column(db.String(50))
    semester = db.Column(db.String(20))
    academic_year = db.Column(db.String(20))
    
    faculty = db.relationship('User', backref='schedules')


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # workload, attendance, marks, etc.
    generated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(300))
    parameters = db.Column(db.Text)  # JSON string of report parameters
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    generator = db.relationship('User', backref='generated_reports')


class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    description = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    updater = db.relationship('User')


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    old_values = db.Column(db.Text)  # JSON string
    new_values = db.Column(db.Text)  # JSON string
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    user = db.relationship('User', backref='audit_logs')


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_role = db.Column(db.String(20), nullable=False)  # 'faculty', 'student', 'all'
    priority = db.Column(db.String(10), default='normal')  # 'high', 'normal', 'low'
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='announcements')


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100))
    semester = db.Column(db.String(20))
    credits = db.Column(db.Integer, default=3)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FacultySubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    academic_year = db.Column(db.String(20))
    semester = db.Column(db.String(20))
    class_section = db.Column(db.String(10))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    faculty = db.relationship('User', foreign_keys=[faculty_id], backref='assigned_subjects')
    subject = db.relationship('Subject', backref='faculty_assignments')
    assigner = db.relationship('User', foreign_keys=[assigned_by])


class TestMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_number = db.Column(db.Integer, nullable=False)  # 1-5 for 5 tests
    marks_obtained = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    test_date = db.Column(db.Date)
    remarks = db.Column(db.Text)
    proof_file_path = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='test_marks')
    subject = db.relationship('Subject', backref='test_marks')
    faculty = db.relationship('User', foreign_keys=[faculty_id])


class LabPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lab_session = db.Column(db.String(100), nullable=False)
    performance_score = db.Column(db.Float, nullable=False)  # Out of 10
    attendance = db.Column(db.String(10), default='Present')  # Present, Absent
    practical_marks = db.Column(db.Float)
    viva_marks = db.Column(db.Float)
    assignment_marks = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    comments = db.Column(db.Text)
    lab_date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='lab_performances')
    subject = db.relationship('Subject', backref='lab_performances')
    faculty = db.relationship('User', foreign_keys=[faculty_id])


class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    file_type = db.Column(db.String(50))  # pdf, doc, ppt, etc.
    download_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject = db.relationship('Subject', backref='study_materials')
    uploader = db.relationship('User', backref='uploaded_materials')


class StudentFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    # 10 Feedback Questions
    teaching_clarity = db.Column(db.Integer, nullable=False)  # 1-5 rating
    subject_knowledge = db.Column(db.Integer, nullable=False)
    communication_skills = db.Column(db.Integer, nullable=False)
    punctuality = db.Column(db.Integer, nullable=False)
    assignment_feedback = db.Column(db.Integer, nullable=False)
    doubt_resolution = db.Column(db.Integer, nullable=False)
    course_completion = db.Column(db.Integer, nullable=False)
    practical_approach = db.Column(db.Integer, nullable=False)
    student_interaction = db.Column(db.Integer, nullable=False)
    overall_satisfaction = db.Column(db.Integer, nullable=False)
    
    additional_comments = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='given_feedback')
    faculty = db.relationship('User', foreign_keys=[faculty_id], backref='received_feedback')
    subject = db.relationship('Subject', backref='feedback_records')


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Float, default=100)
    file_path = db.Column(db.String(300))  # Assignment file
    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject = db.relationship('Subject', backref='assignments')
    faculty = db.relationship('User', backref='created_assignments')


class AssignmentSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    submission_text = db.Column(db.Text)
    marks_obtained = db.Column(db.Float)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20), default='Submitted')  # Submitted, Graded, Late
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded_at = db.Column(db.DateTime)
    
    assignment = db.relationship('Assignment', backref='submissions')
    student = db.relationship('User', backref='assignment_submissions')


class ExamTimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # Unit Test, Semester Exam
    exam_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    room_number = db.Column(db.String(50))
    max_marks = db.Column(db.Float, default=100)
    instructions = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject = db.relationship('Subject', backref='exam_schedule')
    creator = db.relationship('User', backref='created_exams')


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), default='Present')  # Present, Absent, Late
    lecture_type = db.Column(db.String(20), default='Theory')  # Theory, Practical, Tutorial
    remarks = db.Column(db.Text)
    marked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='attendance_records')
    subject = db.relationship('Subject', backref='subject_attendance_records')
    faculty = db.relationship('User', foreign_keys=[faculty_id])
    marker = db.relationship('User', foreign_keys=[marked_by])


# Example function to create users (run this separately in shell or script)
def create_sample_users():
    from extension import db
    hod = User(username='hoduser', role='hod')
    hod.set_password('hodpass')

    cc = User(username='ccuser', role='cc')
    cc.set_password('ccpass')

    faculty = User(username='facultyuser', role='faculty')
    faculty.set_password('facultypass')

    student = User(username='studentuser', role='student')
    student.set_password('studentpass')

    db.session.add_all([hod, cc, faculty, student])
    db.session.commit()


class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # HOD for faculty, CC for students
    leave_type = db.Column(db.String(50), nullable=False)  # sick, casual, emergency, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    comments = db.Column(db.Text)  # Approver comments
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='leave_requests')
    approver = db.relationship('User', foreign_keys=[approver_id], backref='approved_leaves')
    approver = db.relationship('User', foreign_keys=[approver_id])


class ModelAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False)  # OOP, DMs, DTM, etc.
    subject_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(20))  # pdf, doc, txt, etc.
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    semester = db.Column(db.String(20))
    academic_year = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    uploader = db.relationship('User', backref='uploaded_model_answers')
