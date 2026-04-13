from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from extension import db
from forms import (LoginForm, ComplaintForm, FeedbackForm, WorkloadForm, MarksForm, 
                  ProfileForm, AttendanceForm, ScheduleForm, ReportForm, SearchForm, 
                  ChangePasswordForm, SystemSettingsForm, AnnouncementForm, SubjectForm,
                  AssignSubjectForm, TestMarksForm, LabPerformanceForm, StudyMaterialForm,
                  DetailedFeedbackForm, AssignmentForm, AssignmentSubmissionForm,
                  ExamTimetableForm, StudentAttendanceForm)
from models import (User, Complaint, Workload, Marks, Notification, Attendance, 
                   Schedule, Report, SystemSettings, AuditLog, Announcement, Subject,
                   FacultySubject, TestMarks, LabPerformance, StudyMaterial, StudentFeedback,
                   Assignment, AssignmentSubmission, ExamTimetable, StudentAttendance)
from utils import (get_dashboard_stats, save_profile_picture, calculate_hours_worked,
                  generate_workload_report, generate_attendance_report, export_to_csv,
                  send_email_notification, log_user_action, search_records, 
                  get_weekly_schedule, calculate_workload_distribution, get_marks_analytics)
from datetime import datetime, date, time
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faculty_workload.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize db with app
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user)
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log login action
            log_user_action(user.id, 'LOGIN', ip_address=request.remote_addr)
            
            flash(f"Welcome {user.full_name or user.username}!", "success")
            if user.role == 'hod':
                return redirect(url_for('hod_dashboard'))
            elif user.role == 'cc':
                return redirect(url_for('cc_dashboard'))
            elif user.role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password, or account is deactivated', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# HOD Dashboard
@app.route('/hod_dashboard')
@login_required
def hod_dashboard():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    stats = get_dashboard_stats('hod')
    workload_distribution = calculate_workload_distribution()
    marks_analytics = get_marks_analytics()
    
    return render_template('hod_dashboard.html', 
                         stats=stats, 
                         workload_distribution=workload_distribution,
                         marks_analytics=marks_analytics)

@app.route('/hod_dashboard/assign_workload', methods=['GET', 'POST'])
@login_required
def assign_workload():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    form = WorkloadForm()
    form.faculty.choices = [(f.id, f.username) for f in User.query.filter_by(role='faculty').all()]

    if form.validate_on_submit():
        workload = Workload(
            faculty_id=form.faculty.data,
            subject=form.subject.data,
            hours=form.hours.data,
            assigned_by=current_user.id
        )
        db.session.add(workload)
        
        # Create notification for faculty
        faculty = User.query.get(form.faculty.data)
        notification = Notification(
            user_id=form.faculty.data,
            title="New Workload Assignment",
            message=f"You have been assigned a new subject: {form.subject.data} ({form.hours.data} hours/week)"
        )
        db.session.add(notification)
        db.session.commit()
        
        flash(f"Workload assigned successfully to {faculty.username}. Notification sent.", "success")
        return redirect(url_for('hod_dashboard'))

    return render_template('hod/assign_workload.html', form=form)

# CC Dashboard
@app.route('/cc_dashboard')
@login_required
def cc_dashboard():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get recent announcements and complaints for dashboard
    recent_announcements = Announcement.query.filter_by(created_by=current_user.id).order_by(Announcement.timestamp.desc()).limit(5).all()
    pending_complaints = Complaint.query.filter_by(status='Pending').count()
    
    return render_template('cc_dashboard.html', 
                         recent_announcements=recent_announcements,
                         pending_complaints=pending_complaints)

# HOD - Announcements for Faculty
@app.route('/hod_dashboard/announcements', methods=['GET', 'POST'])
@login_required
def hod_announcements():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            target_role=form.target_role.data,
            priority=form.priority.data,
            expires_at=form.expires_at.data,
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('hod_announcements'))
    
    announcements = Announcement.query.filter_by(author_id=current_user.id).order_by(Announcement.timestamp.desc()).all()
    return render_template('hod/announcements.html', form=form, announcements=announcements)

# HOD - Manage Subjects
@app.route('/hod_dashboard/manage_subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            code=form.code.data,
            credits=form.credits.data,
            semester=form.semester.data,
            department=form.department.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
        return redirect(url_for('manage_subjects'))
    
    subjects = Subject.query.all()
    return render_template('hod/manage_subjects.html', form=form, subjects=subjects)

# HOD - Assign Subject to Faculty
@app.route('/hod_dashboard/assign_subject', methods=['GET', 'POST'])
@login_required
def assign_subject():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    form = SubjectAssignmentForm()
    if form.validate_on_submit():
        assignment = SubjectAssignment(
            faculty_id=form.faculty_id.data,
            subject_id=form.subject_id.data,
            assigned_by=current_user.id
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Subject assigned successfully!', 'success')
        return redirect(url_for('assign_subject'))
    
    assignments = SubjectAssignment.query.all()
    return render_template('hod/assign_subject.html', form=form, assignments=assignments)

# HOD - Manage Test Marks (removed duplicate - using the one below with POST support)

# HOD - View Complaints
@app.route('/hod_dashboard/view_complaints')
@login_required
def hod_view_complaints():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    complaints = Complaint.query.all()
    return render_template('hod/view_complaints.html', complaints=complaints)

# HOD - Generate Reports
@app.route('/hod_dashboard/generate_reports')
@login_required
def generate_reports():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    return render_template('hod/generate_reports.html')

# Profile and Password Change Routes (removed simple version - using the one below with POST support)

# Change password route (removed duplicate - using the one below)

# CC - Announcements for Students
@app.route('/cc_dashboard/announcements', methods=['GET', 'POST'])
@login_required
def cc_announcements():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            created_by=current_user.id,
            target_role='student',  # CC announcements are for students
            priority=form.priority.data,
            expires_at=form.expires_at.data
        )
        db.session.add(announcement)
        db.session.commit()
        flash("Announcement created successfully!", "success")
        return redirect(url_for('cc_announcements'))
    
    announcements = Announcement.query.filter_by(created_by=current_user.id, target_role='student').order_by(Announcement.timestamp.desc()).all()
    return render_template('cc/announcements.html', form=form, announcements=announcements)

# CC - Edit Announcement
@app.route('/cc_dashboard/edit_announcement/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def cc_edit_announcement(announcement_id):
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    announcement = Announcement.query.get_or_404(announcement_id)
    form = AnnouncementForm(obj=announcement)
    
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        announcement.priority = form.priority.data
        announcement.expires_at = form.expires_at.data
        db.session.commit()
        flash("Announcement updated successfully!", "success")
        return redirect(url_for('cc_announcements'))
    
    return render_template('cc/edit_announcement.html', form=form, announcement=announcement)

# CC - Delete Announcement
@app.route('/cc_dashboard/delete_announcement/<int:announcement_id>', methods=['POST'])
@login_required
def cc_delete_announcement(announcement_id):
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    flash("Announcement deleted successfully!", "success")
    return redirect(url_for('cc_announcements'))

@app.route('/cc_dashboard/view_complaints')
@login_required
def view_complaints():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    complaints = Complaint.query.filter_by(status='Pending').all()
    return render_template('cc/view_complaints.html', complaints=complaints)

@app.route('/cc_dashboard/resolve_complaint/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
def resolve_complaint(complaint_id):
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    complaint = Complaint.query.get_or_404(complaint_id)
    form = FeedbackForm()

    if form.validate_on_submit():
        complaint.feedback = form.feedback.data
        complaint.status = 'Resolved'
        complaint.cc_id = current_user.id
        db.session.commit()
        flash("Complaint resolved and feedback sent", "success")
        return redirect(url_for('view_complaints'))

    return render_template('cc/resolve_complaint.html', form=form, complaint=complaint)

@app.route('/cc_dashboard/send_marks', methods=['GET', 'POST'])
@login_required
def send_marks():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    form = MarksForm()
    form.student.choices = [(s.id, s.username) for s in User.query.filter_by(role='student').all()]

    if form.validate_on_submit():
        marks = Marks(
            student_id=form.student.data,
            cc_id=current_user.id,
            subject=form.subject.data,
            marks_obtained=form.marks_obtained.data,
            total_marks=form.total_marks.data
        )
        db.session.add(marks)
        db.session.commit()
        flash("Marks sent to HOD successfully.", "success")
        return redirect(url_for('cc_dashboard'))

    return render_template('cc/send_marks.html', form=form)

# HOD view marks pie chart
@app.route('/hod_dashboard/view_marks_chart')
@login_required
def view_marks_chart():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    marks = Marks.query.all()

    subject_totals = {}
    subject_obtained = {}

    for m in marks:
        subject_totals[m.subject] = subject_totals.get(m.subject, 0) + m.total_marks
        subject_obtained[m.subject] = subject_obtained.get(m.subject, 0) + m.marks_obtained

    labels = list(subject_totals.keys())
    data = [round((subject_obtained[sub] / subject_totals[sub]) * 100, 2) if subject_totals[sub] != 0 else 0 for sub in labels]

    return render_template('hod/view_marks_chart.html', labels=labels, data=data)

# HOD view all workloads
@app.route('/hod_dashboard/view_workloads')
@login_required
def hod_view_workloads():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    workloads = Workload.query.all()
    return render_template('hod/view_workloads.html', workloads=workloads)

# HOD - Test Marks Management
@app.route('/hod_dashboard/test_marks', methods=['GET', 'POST'])
@login_required
def manage_test_marks():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = TestMarksForm()
    form.student.choices = [(s.id, s.full_name or s.username) for s in User.query.filter_by(role='student', is_active=True).all()]
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in Subject.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        test_marks = TestMarks(
            student_id=form.student.data,
            subject_id=form.subject.data,
            faculty_id=current_user.id,
            test_number=form.test_number.data,
            marks_obtained=form.marks_obtained.data,
            total_marks=form.total_marks.data,
            test_date=form.test_date.data,
            remarks=form.remarks.data
        )
        db.session.add(test_marks)
        db.session.commit()
        flash("Test marks added successfully!", "success")
        return redirect(url_for('manage_test_marks'))
    
    # Get all test marks for viewing
    test_marks = TestMarks.query.order_by(TestMarks.timestamp.desc()).all()
    return render_template('hod/test_marks.html', form=form, test_marks=test_marks)

# HOD - View Student Complaints (removed duplicate - using the one above)

# Faculty Dashboard
@app.route('/faculty_dashboard')
@login_required
def faculty_dashboard():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get HOD announcements for faculty
    announcements = Announcement.query.filter(
        (Announcement.target_role == 'faculty') | (Announcement.target_role == 'all')
    ).filter_by(is_active=True).order_by(Announcement.timestamp.desc()).limit(5).all()
    
    # Get assigned subjects
    assigned_subjects = FacultySubject.query.filter_by(faculty_id=current_user.id).all()
    
    return render_template('faculty_dashboard.html', announcements=announcements, assigned_subjects=assigned_subjects)

@app.route('/faculty_dashboard/view_workload')
@login_required
def view_workload():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    workloads = Workload.query.filter_by(faculty_id=current_user.id).all()
    return render_template('faculty/view_workload.html', workloads=workloads)

# Student Dashboard
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get CC announcements for students
    announcements = Announcement.query.filter(
        (Announcement.target_role == 'student') | (Announcement.target_role == 'all')
    ).filter_by(is_active=True).order_by(Announcement.timestamp.desc()).limit(5).all()
    
    # Get recent test marks
    recent_marks = TestMarks.query.filter_by(student_id=current_user.id).order_by(TestMarks.timestamp.desc()).limit(5).all()
    
    # Get lab performance records
    lab_performance = LabPerformance.query.filter_by(student_id=current_user.id).order_by(LabPerformance.timestamp.desc()).limit(5).all()
    
    return render_template('student_dashboard.html', 
                         announcements=announcements,
                         recent_marks=recent_marks,
                         lab_performance=lab_performance)

@app.route('/student_dashboard/complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(student_id=current_user.id, content=form.content.data)
        db.session.add(complaint)
        db.session.commit()
        flash("Complaint sent to CC successfully", "success")
        return redirect(url_for('student_dashboard'))

    return render_template('student/submit_complaint.html', form=form)

# Student Routes - Detailed Feedback (10 Questions)
@app.route('/student_dashboard/feedback', methods=['GET', 'POST'])
@login_required
def student_feedback():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = DetailedFeedbackForm()
    form.faculty.choices = [(f.id, f.full_name or f.username) for f in User.query.filter_by(role='faculty', is_active=True).all()]
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in Subject.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        feedback = StudentFeedback(
            student_id=current_user.id,
            faculty_id=form.faculty.data,
            subject_id=form.subject.data,
            teaching_clarity=form.teaching_clarity.data,
            subject_knowledge=form.subject_knowledge.data,
            communication_skills=form.communication_skills.data,
            punctuality=form.punctuality.data,
            assignment_feedback=form.assignment_feedback.data,
            doubt_resolution=form.doubt_resolution.data,
            course_completion=form.course_completion.data,
            practical_approach=form.practical_approach.data,
            student_interaction=form.student_interaction.data,
            overall_satisfaction=form.overall_satisfaction.data,
            additional_comments=form.additional_comments.data,
            suggestions=form.suggestions.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Detailed feedback submitted successfully!", "success")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/feedback_form.html', form=form)

# Student - View Study Materials
@app.route('/student_dashboard/study_materials')
@login_required
def student_study_materials():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    materials = StudyMaterial.query.filter_by(is_active=True).order_by(StudyMaterial.timestamp.desc()).all()
    return render_template('student/study_materials.html', materials=materials)

# Student - Download Study Material
@app.route('/download_material/<int:material_id>')
@login_required
def download_material(material_id):
    material = StudyMaterial.query.get_or_404(material_id)
    
    # Increment download count
    material.download_count += 1
    db.session.commit()
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], material.file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=material.file_name)
    else:
        flash('File not found.', 'danger')
        return redirect(url_for('student_study_materials'))

# Student - View Announcements
@app.route('/student_dashboard/announcements')
@login_required
def student_announcements():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    announcements = Announcement.query.filter(
        (Announcement.target_role == 'student') | (Announcement.target_role == 'all')
    ).filter_by(is_active=True).order_by(Announcement.timestamp.desc()).all()
    
    return render_template('student/announcements.html', announcements=announcements)

# Student - View Test Marks
@app.route('/student_dashboard/test_marks')
@login_required
def student_test_marks():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    test_marks = TestMarks.query.filter_by(student_id=current_user.id).order_by(TestMarks.timestamp.desc()).all()
    return render_template('student/test_marks.html', test_marks=test_marks)

# Student - View Lab Performance
@app.route('/student_dashboard/lab_performance')
@login_required
def student_lab_performance():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    lab_records = LabPerformance.query.filter_by(student_id=current_user.id).order_by(LabPerformance.timestamp.desc()).all()
    return render_template('student/lab_performance.html', lab_records=lab_records)

@app.route('/student_dashboard/marks')
@login_required
def view_student_marks():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get both old marks and new test marks
    old_marks = Marks.query.filter_by(student_id=current_user.id).all()
    test_marks = TestMarks.query.filter_by(student_id=current_user.id).order_by(TestMarks.timestamp.desc()).all()
    
    return render_template('student/view_marks.html', old_marks=old_marks, test_marks=test_marks)

# Profile Management Routes
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.department = form.department.data
        
        if form.profile_picture.data:
            picture_path = save_profile_picture(form.profile_picture.data)
            if picture_path:
                current_user.profile_picture = picture_path
        
        db.session.commit()
        log_user_action(current_user.id, 'UPDATE_PROFILE')
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-populate form with current user data
    form.full_name.data = current_user.full_name
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    form.department.data = current_user.department
    
    return render_template('profile.html', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            if form.new_password.data == form.confirm_password.data:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                log_user_action(current_user.id, 'CHANGE_PASSWORD')
                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('New passwords do not match!', 'danger')
        else:
            flash('Current password is incorrect!', 'danger')
    
    return render_template('change_password.html', form=form)

# Attendance Management Routes
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def manage_attendance():
    if current_user.role not in ['hod', 'cc']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = AttendanceForm()
    form.user.choices = [(u.id, f"{u.username} ({u.role})") for u in User.query.filter(User.role.in_(['faculty', 'student'])).all()]
    
    if form.validate_on_submit():
        # Check if attendance already exists for this user and date
        existing = Attendance.query.filter_by(
            user_id=form.user.data,
            date=form.date.data
        ).first()
        
        if existing:
            flash('Attendance already recorded for this user on this date!', 'warning')
        else:
            check_in_datetime = None
            check_out_datetime = None
            
            if form.check_in.data:
                check_in_datetime = datetime.combine(form.date.data, form.check_in.data)
            if form.check_out.data:
                check_out_datetime = datetime.combine(form.date.data, form.check_out.data)
            
            hours_worked = calculate_hours_worked(check_in_datetime, check_out_datetime)
            
            attendance = Attendance(
                user_id=form.user.data,
                date=form.date.data,
                check_in=check_in_datetime,
                check_out=check_out_datetime,
                status=form.status.data,
                hours_worked=hours_worked,
                notes=form.notes.data
            )
            
            db.session.add(attendance)
            db.session.commit()
            log_user_action(current_user.id, 'RECORD_ATTENDANCE', 'attendance', attendance.id)
            flash('Attendance recorded successfully!', 'success')
            return redirect(url_for('manage_attendance'))
    
    # Get recent attendance records
    recent_attendance = Attendance.query.order_by(Attendance.date.desc()).limit(10).all()
    
    return render_template('attendance.html', form=form, recent_attendance=recent_attendance)

@app.route('/my_attendance')
@login_required
def my_attendance():
    attendance_records = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.date.desc()).all()
    return render_template('my_attendance.html', attendance_records=attendance_records)

# Schedule Management Routes
@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def manage_schedule():
    if current_user.role not in ['hod', 'cc']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ScheduleForm()
    form.faculty.choices = [(f.id, f.username) for f in User.query.filter_by(role='faculty').all()]
    
    if form.validate_on_submit():
        # Check for time conflicts
        existing_schedule = Schedule.query.filter_by(
            faculty_id=form.faculty.data,
            day_of_week=form.day_of_week.data
        ).filter(
            db.or_(
                db.and_(Schedule.start_time <= form.start_time.data, Schedule.end_time > form.start_time.data),
                db.and_(Schedule.start_time < form.end_time.data, Schedule.end_time >= form.end_time.data)
            )
        ).first()
        
        if existing_schedule:
            flash('Time conflict detected! Faculty already has a class at this time.', 'danger')
        else:
            schedule = Schedule(
                faculty_id=form.faculty.data,
                subject=form.subject.data,
                day_of_week=form.day_of_week.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                room_number=form.room_number.data,
                semester=form.semester.data,
                academic_year=form.academic_year.data
            )
            
            db.session.add(schedule)
            db.session.commit()
            log_user_action(current_user.id, 'CREATE_SCHEDULE', 'schedule', schedule.id)
            flash('Schedule created successfully!', 'success')
            return redirect(url_for('manage_schedule'))
    
    schedules = Schedule.query.all()
    return render_template('schedule.html', form=form, schedules=schedules)

@app.route('/my_schedule')
@login_required
def my_schedule():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    weekly_schedule = get_weekly_schedule(current_user.id)
    return render_template('my_schedule.html', weekly_schedule=weekly_schedule)

# Report Generation Routes
@app.route('/reports', methods=['GET', 'POST'])
@login_required
def generate_reports():
    if current_user.role not in ['hod', 'cc']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ReportForm()
    
    if form.validate_on_submit():
        report_data = []
        
        if form.report_type.data == 'workload':
            report_data = generate_workload_report(form.date_from.data, form.date_to.data)
        elif form.report_type.data == 'attendance':
            report_data = generate_attendance_report(form.date_from.data, form.date_to.data)
        elif form.report_type.data == 'marks':
            marks = Marks.query
            if form.date_from.data:
                marks = marks.filter(Marks.timestamp >= form.date_from.data)
            if form.date_to.data:
                marks = marks.filter(Marks.timestamp <= form.date_to.data)
            
            report_data = [{
                'Student': mark.student.username,
                'Subject': mark.subject,
                'Marks Obtained': mark.marks_obtained,
                'Total Marks': mark.total_marks,
                'Percentage': round((mark.marks_obtained / mark.total_marks) * 100, 2),
                'Date': mark.timestamp.strftime('%Y-%m-%d')
            } for mark in marks.all()]
        
        if report_data:
            # Export to CSV
            csv_path = export_to_csv(report_data, form.report_type.data + '_report')
            
            # Save report record
            report = Report(
                title=form.title.data,
                report_type=form.report_type.data,
                generated_by=current_user.id,
                file_path=csv_path,
                parameters=json.dumps({
                    'date_from': form.date_from.data.isoformat() if form.date_from.data else None,
                    'date_to': form.date_to.data.isoformat() if form.date_to.data else None
                })
            )
            
            db.session.add(report)
            db.session.commit()
            log_user_action(current_user.id, 'GENERATE_REPORT', 'report', report.id)
            
            flash(f'Report generated successfully! <a href="{url_for("download_report", report_id=report.id)}">Download</a>', 'success')
        else:
            flash('No data found for the specified criteria.', 'warning')
    
    # Get recent reports
    recent_reports = Report.query.order_by(Report.timestamp.desc()).limit(10).all()
    
    return render_template('reports.html', form=form, recent_reports=recent_reports)

@app.route('/download_report/<int:report_id>')
@login_required
def download_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if current_user.role not in ['hod', 'cc'] and report.generated_by != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    file_path = os.path.join(app.root_path, 'static', report.file_path)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('Report file not found.', 'danger')
        return redirect(url_for('generate_reports'))

# Search Functionality
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = None
    
    if form.validate_on_submit():
        results = search_records(form.query.data, form.search_type.data)
        log_user_action(current_user.id, 'SEARCH', parameters={'query': form.query.data, 'type': form.search_type.data})
    
    return render_template('search.html', form=form, results=results)

# API Routes for AJAX requests
@app.route('/api/dashboard_stats')
@login_required
def api_dashboard_stats():
    stats = get_dashboard_stats(current_user.role, current_user.id)
    return jsonify(stats)

@app.route('/api/mark_notification_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 403

# System Settings (HOD only)
@app.route('/system_settings', methods=['GET', 'POST'])
@login_required
def system_settings():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = SystemSettingsForm()
    
    if form.validate_on_submit():
        setting = SystemSettings.query.filter_by(setting_key=form.setting_key.data).first()
        
        if setting:
            setting.setting_value = form.setting_value.data
            setting.description = form.description.data
            setting.updated_by = current_user.id
            setting.updated_at = datetime.utcnow()
        else:
            setting = SystemSettings(
                setting_key=form.setting_key.data,
                setting_value=form.setting_value.data,
                description=form.description.data,
                updated_by=current_user.id
            )
            db.session.add(setting)
        
        db.session.commit()
        log_user_action(current_user.id, 'UPDATE_SYSTEM_SETTING', 'system_settings', setting.id)
        flash('System setting updated successfully!', 'success')
        return redirect(url_for('system_settings'))
    
    settings = SystemSettings.query.all()
    return render_template('system_settings.html', form=form, settings=settings)

# Audit Log (HOD only)
@app.route('/audit_log')
@login_required
def audit_log():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('audit_log.html', logs=logs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # tables create होण्यासाठी ही ओळ फार महत्त्वाची आहे
    app.run(debug=True)
