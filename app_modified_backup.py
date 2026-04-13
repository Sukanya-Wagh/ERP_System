from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from extension import db
from forms import (LoginForm, ComplaintForm, FeedbackForm, WorkloadForm, MarksForm, 
                  ProfileForm, AttendanceForm, ScheduleForm, ReportForm, SearchForm, 
                  ChangePasswordForm, SystemSettingsForm, AnnouncementForm, SubjectForm,
                  AssignSubjectForm, TestMarksForm, LabPerformanceForm, StudyMaterialForm,
                  DetailedFeedbackForm, AssignmentForm, AssignmentSubmissionForm,
                  ExamTimetableForm, StudentAttendanceForm, SubjectAssignmentForm,
                  LeaveRequestForm, LeaveApprovalForm, ModelAnswerForm, ImportMarksForm,
                  ManageMarksForm)
import pandas as pd
import io
from werkzeug.utils import secure_filename
import os
from models import (User, Complaint, Workload, Marks, Notification, Attendance, 
                   Schedule, Report, SystemSettings, AuditLog, Announcement, Subject,
                   FacultySubject, TestMarks, LabPerformance, StudyMaterial, StudentFeedback,
                   Assignment, AssignmentSubmission, ExamTimetable, StudentAttendance, LeaveRequest, ModelAnswer)
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
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            if user.role == 'hod':
                return redirect(url_for('hod_dashboard'))
            elif user.role == 'cc':
                return redirect(url_for('cc_dashboard'))
            elif user.role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# HOD Dashboard
@app.route('/hod_dashboard')
@login_required
def hod_dashboard():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get dashboard statistics
    faculty_count = User.query.filter_by(role='faculty', is_active=True).count()
    subject_count = Subject.query.filter_by(is_active=True).count()
    complaint_count = Complaint.query.filter_by(status='Pending').count()
    announcement_count = Announcement.query.filter_by(created_by=current_user.id, is_active=True).count()
    
    return render_template('hod_dashboard.html',
                         faculty_count=faculty_count,
                         subject_count=subject_count,
                         complaint_count=complaint_count,
                         announcement_count=announcement_count,
                         current_year=datetime.now().year)

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
            created_by=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('hod_announcements'))
    
    announcements = Announcement.query.filter_by(created_by=current_user.id).order_by(Announcement.timestamp.desc()).all()
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
        assignment = FacultySubject(
            faculty_id=form.faculty_id.data,
            subject_id=form.subject_id.data,
            assigned_by=current_user.id
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Subject assigned successfully!', 'success')
        return redirect(url_for('assign_subject'))
    
    assignments = FacultySubject.query.all()
    return render_template('hod/assign_subject.html', form=form, assignments=assignments)

# HOD - Manage Test Marks
@app.route('/hod_dashboard/manage_test_marks', methods=['GET', 'POST'])
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
    return render_template('hod/manage_test_marks.html', form=form, test_marks=test_marks)

# HOD - View Complaints
@app.route('/hod_dashboard/view_complaints')
@login_required
def hod_view_complaints():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    complaints = Complaint.query.all()
    return render_template('hod/view_complaints.html', complaints=complaints)

# HOD - View Staff Records (2020-2025)
@app.route('/hod/view_staff_records')
@login_required
def hod_view_staff_records():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get all faculty members with their subjects and leave records
    staff_list = db.session.query(
        User,
        db.func.group_concat(Subject.name.distinct()).label('subjects_taught'),
        db.func.count(LeaveRequest.id).label('total_leaves')
    ).outerjoin(
        FacultySubject, User.id == FacultySubject.faculty_id
    ).outerjoin(
        Subject, FacultySubject.subject_id == Subject.id
    ).outerjoin(
        LeaveRequest, (User.id == LeaveRequest.user_id) & 
        (LeaveRequest.status == 'Approved') &
        (LeaveRequest.start_date.between('2020-01-01', '2025-12-31'))
    ).filter(
        User.role == 'faculty'
    ).group_by(
        User.id
    ).all()
    
    return render_template('hod/staff_records.html', 
                         staff_list=staff_list,
                         current_year=datetime.now().year)

# HOD - View Staff
@app.route('/hod/view_staff')
@login_required
def hod_view_staff():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    staff_list = User.query.filter_by(role='faculty').all()
    return render_template('hod/view_staff.html', staff_list=staff_list)

# HOD - View Workloads
@app.route('/hod_dashboard/view_workloads')
@login_required
def hod_view_workloads():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    workloads = Workload.query.all()
    return render_template('hod/view_workloads.html', workloads=workloads)

# HOD - Generate Reports
@app.route('/hod_dashboard/generate_reports', methods=['GET', 'POST'])
@login_required
def generate_reports():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        
        # Generate actual report file
        import os
        from datetime import datetime
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(app.static_folder, 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type.replace(' ', '_')}_{timestamp}.txt"
        filepath = os.path.join(exports_dir, filename)
        
        # Create sample report content
        report_content = f"""
{report_type} Report
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

Report Summary:
- Total Records: {User.query.count() if 'Faculty' in report_type else 'N/A'}
- Report Type: {report_type}
- Status: Generated Successfully

This is a sample report. In a production system, this would contain
detailed data based on the selected report type and parameters.
"""
        
        # Write report to file
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        flash(f'{report_type} report generated successfully! <a href="/static/exports/{filename}" target="_blank">Download Report</a>', 'success')
        return redirect(url_for('generate_reports'))
    
    return render_template('hod/generate_reports.html')

# Profile Management
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
            filename = secure_filename(form.profile_picture.data.filename)
            if filename:
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                form.profile_picture.data.save(file_path)
                current_user.profile_picture = f'uploads/profiles/{filename}'
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-populate form with current user data
    form.full_name.data = current_user.full_name
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    form.department.data = current_user.department
    
    return render_template('profile.html', form=form)

# Change Password
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            if form.new_password.data == form.confirm_password.data:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('New passwords do not match.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('change_password.html', form=form)

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
            target_role='student',
            priority=form.priority.data,
            expires_at=form.expires_at.data,
            created_by=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash("Announcement created successfully!", "success")
        return redirect(url_for('cc_announcements'))
    
    announcements = Announcement.query.filter_by(created_by=current_user.id).order_by(Announcement.timestamp.desc()).all()
    return render_template('cc/announcements.html', form=form, announcements=announcements)

# CC - Send Marks
@app.route('/cc_dashboard/send_marks', methods=['GET', 'POST'])
@login_required
def send_marks():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = MarksForm()
    # Populate student choices
    students = User.query.filter_by(role='student').all()
    form.student.choices = [(student.id, f"{student.full_name or student.username} ({student.username})") for student in students]
    
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
        flash("Marks sent successfully!", "success")
        return redirect(url_for('send_marks'))
    
    return render_template('cc/send_marks.html', form=form)

# CC - View Complaints
@app.route('/cc_dashboard/view_complaints')
@login_required
def cc_view_complaints():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    complaints = Complaint.query.all()
    return render_template('cc/view_complaints.html', complaints=complaints)

# CC - Resolve Complaint
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
        flash("Complaint resolved successfully!", "success")
        return redirect(url_for('cc_view_complaints'))
    
    return render_template('cc/resolve_complaints.html', form=form, complaint=complaint)

# CC - Leave Requests (for students)
@app.route('/cc_dashboard/leave_requests')
@login_required
def cc_leave_requests():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Debug: Check current user and all leave requests
    print(f"Current CC user ID: {current_user.id}")
    all_requests = LeaveRequest.query.all()
    print(f"Total leave requests in database: {len(all_requests)}")
    for req in all_requests:
        print(f"Request ID: {req.id}, User: {req.user_id}, Approver: {req.approver_id}, Status: {req.status}")
    
    leave_requests = LeaveRequest.query.filter_by(approver_id=current_user.id).all()
    print(f"Leave requests for CC {current_user.id}: {len(leave_requests)}")
    
    return render_template('cc/leave_requests.html', leave_requests=leave_requests)

@app.route('/cc_dashboard/approve_leave/<int:request_id>', methods=['GET', 'POST'])
@login_required
def cc_approve_leave(request_id):
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    leave_request = LeaveRequest.query.get_or_404(request_id)
    form = LeaveApprovalForm()
    
    if form.validate_on_submit():
        leave_request.status = form.status.data
        leave_request.comments = form.comments.data
        leave_request.approver_id = current_user.id
        db.session.commit()
        flash(f"Leave request {form.status.data.lower()} successfully!", "success")
        return redirect(url_for('cc_leave_requests'))
    
    return render_template('cc/approve_leave.html', form=form, leave_request=leave_request)

# HOD - Leave Requests (for faculty)
@app.route('/hod_dashboard/leave_requests')
@login_required
def hod_leave_requests():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Debug: Check current user and all leave requests
    print(f"Current HOD user ID: {current_user.id}")
    all_requests = LeaveRequest.query.all()
    print(f"Total leave requests in database: {len(all_requests)}")
    for req in all_requests:
        print(f"Request ID: {req.id}, User: {req.user_id}, Approver: {req.approver_id}, Status: {req.status}")
    
    leave_requests = LeaveRequest.query.filter_by(approver_id=current_user.id).all()
    print(f"Leave requests for HOD {current_user.id}: {len(leave_requests)}")
    
    return render_template('hod/leave_requests.html', leave_requests=leave_requests)

@app.route('/hod_dashboard/approve_leave/<int:request_id>', methods=['GET', 'POST'])
@login_required
def hod_approve_leave(request_id):
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    leave_request = LeaveRequest.query.get_or_404(request_id)
    form = LeaveApprovalForm()
    
    if form.validate_on_submit():
        leave_request.status = form.status.data
        leave_request.comments = form.comments.data
        leave_request.approver_id = current_user.id
        db.session.commit()
        flash(f"Leave request {form.status.data.lower()} successfully!", "success")
        return redirect(url_for('hod_leave_requests'))
    
    return render_template('hod/approve_leave.html', form=form, leave_request=leave_request)

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
    
    return render_template('faculty_dashboard.html', announcements=announcements)

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
    
    return render_template('student_dashboard.html', announcements=announcements)

# Add Staff (HOD only)
@app.route('/add_staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
        else:
            user = User(
                username=username,
                role=role,
                full_name=full_name,
                email=email,
                is_active=True
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash(f"{role.title()} added successfully!", "success")
    
    # Get all staff for display
    staff = User.query.filter(User.role.in_(['faculty', 'cc'])).all()
    return render_template('hod/add_staff.html', users=staff)

# Remove Staff (HOD only)
@app.route('/remove_staff', methods=['POST'])
@login_required
def remove_staff():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    
    if user and user.role in ['faculty', 'cc']:
        try:
            # Delete related audit log entries first to avoid foreign key constraint issues
            AuditLog.query.filter_by(user_id=user.id).delete()
            
            # Delete other related records that might reference this user
            # Delete workloads assigned to this user
            Workload.query.filter_by(faculty_id=user.id).delete()
            
            # Delete marks sent by this user (if CC)
            Marks.query.filter_by(cc_id=user.id).delete()
            
            # Delete notifications for this user
            Notification.query.filter_by(user_id=user.id).delete()
            
            # Delete announcements created by this user
            Announcement.query.filter_by(created_by=user.id).delete()
            
            # Delete faculty-subject assignments
            FacultySubject.query.filter_by(faculty_id=user.id).delete()
            
            # Delete test marks for this user (if student) or created by this user (if faculty)
            TestMarks.query.filter_by(student_id=user.id).delete()
            TestMarks.query.filter_by(faculty_id=user.id).delete()
            
            # Delete lab performance records
            LabPerformance.query.filter_by(student_id=user.id).delete()
            LabPerformance.query.filter_by(faculty_id=user.id).delete()
            
            # Delete study materials uploaded by this user
            StudyMaterial.query.filter_by(uploaded_by=user.id).delete()
            
            # Delete feedback given by or about this user
            StudentFeedback.query.filter_by(student_id=user.id).delete()
            StudentFeedback.query.filter_by(faculty_id=user.id).delete()
            
            # Finally delete the user
            db.session.delete(user)
            db.session.commit()
            flash(f"Staff member {user.username} removed successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error removing staff member: {str(e)}", "error")
    else:
        flash("Staff member not found or cannot be removed", "error")
    
    return redirect(url_for('add_staff'))

# Assign Workload (HOD only)
@app.route('/assign_workload', methods=['GET', 'POST'])
@login_required
def assign_workload():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = WorkloadForm()
    form.faculty.choices = [(f.id, f.full_name or f.username) for f in User.query.filter_by(role='faculty', is_active=True).all()]
    
    if form.validate_on_submit():
        workload = Workload(
            faculty_id=form.faculty.data,
            subject=form.subject.data,
            hours=form.hours.data,
            assigned_by=current_user.id
        )
        db.session.add(workload)
        db.session.commit()
        flash("Workload assigned successfully!", "success")
        return redirect(url_for('assign_workload'))
    
    workloads = Workload.query.all()
    return render_template('hod/assign_workload.html', form=form, workloads=workloads)


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

# Student - Submit Complaint
@app.route('/submit_complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            student_id=current_user.id,
            content=form.content.data,
            status='Pending'
        )
        db.session.add(complaint)
        db.session.commit()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/submit_complaint.html', form=form)

# Faculty - Enter Marks (Batch Entry)
@app.route('/faculty/enter_marks', methods=['GET', 'POST'])
@login_required
def faculty_enter_marks():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ManageMarksForm()
    
    # Get subjects assigned to this faculty
    print(f"\nDEBUG: Getting subjects for faculty_id={current_user.id}")
    faculty_subjects = (Subject.query
                       .join(FacultySubject)
                       .filter(FacultySubject.faculty_id == current_user.id)
                       .order_by(Subject.name)
                       .all())
    
    print(f"DEBUG: Found {len(faculty_subjects)} subjects for faculty")
    for i, subj in enumerate(faculty_subjects, 1):
        print(f"  {i}. {subj.code} - {subj.name} (ID: {subj.id})")
    
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in faculty_subjects]
    
    if form.validate_on_submit():
        # Get all active students
        students = User.query.filter_by(role='student', is_active=True).order_by('roll_number').all()
        subject = Subject.query.get(form.subject.data)
        
        if not students:
            flash('No active students found in the system.', 'warning')
            return redirect(url_for('faculty_enter_marks'))
            
        return render_template('faculty/enter_marks_form.html',
                            students=students,
                            subject=subject,
                            test_number=form.test_number.data,
                            total_marks=form.total_marks.data)
    
    # Get previously entered marks for display
    test_marks = (TestMarks.query
                .join(Subject)
                .filter(TestMarks.faculty_id == current_user.id)
                .order_by(TestMarks.timestamp.desc())
                .limit(10)
                .all())
                               
    return render_template('faculty/enter_marks.html', 
                         form=form, 
                         test_marks=test_marks)

# Faculty - Save Student Marks
@app.route('/faculty/save_marks', methods=['POST'])
@login_required
def save_student_marks():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    subject_id = request.form.get('subject_id')
    test_number = request.form.get('test_number')
    total_marks = float(request.form.get('total_marks'))
    
    # Get all students
    students = User.query.filter_by(role='student', is_active=True).all()
    
    try:
        # Process each student's marks
        for student in students:
            marks_field = f'marks_{student.id}'
            remarks_field = f'remarks_{student.id}'
            
            if marks_field in request.form and request.form[marks_field]:
                marks_obtained = float(request.form[marks_field])
                remarks = request.form.get(remarks_field, '')
                
                # Create or update test marks
                test_marks = TestMarks.query.filter_by(
                    student_id=student.id,
                    subject_id=subject_id,
                    test_number=test_number
                ).first()
                
                if test_marks:
                    # Update existing marks
                    test_marks.marks_obtained = marks_obtained
                    test_marks.total_marks = total_marks
                    test_marks.remarks = remarks
                    test_marks.test_date = datetime.utcnow()
                else:
                    # Create new marks record
                    test_marks = TestMarks(
                        student_id=student.id,
                        subject_id=subject_id,
                        faculty_id=current_user.id,
                        test_number=test_number,
                        marks_obtained=marks_obtained,
                        total_marks=total_marks,
                        remarks=remarks,
                        test_date=datetime.utcnow()
                    )
                    db.session.add(test_marks)
        
        db.session.commit()
        flash('Marks saved successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving marks: {str(e)}', 'error')
    
    return redirect(url_for('faculty_enter_marks'))

# Faculty - Notifications
@app.route('/faculty/notifications')
@login_required
def faculty_notifications():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get personal notifications
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    
    # Get HOD announcements for faculty
    announcements = Announcement.query.filter(
        (Announcement.target_role == 'faculty') | (Announcement.target_role == 'all')
    ).order_by(Announcement.timestamp.desc()).limit(10).all()
    
    return render_template('faculty/notifications.html', notifications=notifications, announcements=announcements)

# Faculty - Send Issue
@app.route('/faculty/send_issue', methods=['GET', 'POST'])
@login_required
def faculty_send_issue():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            student_id=current_user.id,  # Faculty can also submit issues
            content=form.content.data,
            status='Pending'
        )
        db.session.add(complaint)
        db.session.commit()
        flash("Issue submitted successfully!", "success")
        return redirect(url_for('faculty_dashboard'))
    
    return render_template('faculty/send_issue.html', form=form)

# Faculty - Lab Performance
@app.route('/faculty/lab_performance', methods=['GET', 'POST'])
@login_required
def faculty_lab_performance():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = LabPerformanceForm()
    form.student.choices = [(s.id, s.full_name or s.username) for s in User.query.filter_by(role='student', is_active=True).all()]
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in Subject.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        lab_performance = LabPerformance(
            student_id=form.student.data,
            subject_id=form.subject.data,
            faculty_id=current_user.id,
            lab_session=form.lab_session.data,
            performance_score=form.performance_score.data,
            attendance=form.attendance.data,
            practical_marks=form.practical_marks.data,
            viva_marks=form.viva_marks.data,
            assignment_marks=form.assignment_marks.data,
            total_marks=form.total_marks.data,
            comments=form.comments.data,
            lab_date=form.lab_date.data
        )
        db.session.add(lab_performance)
        db.session.commit()
        flash("Lab performance recorded successfully!", "success")
        return redirect(url_for('faculty_lab_performance'))
    
    lab_records = LabPerformance.query.filter_by(faculty_id=current_user.id).order_by(LabPerformance.timestamp.desc()).all()
    return render_template('faculty/lab_performance.html', form=form, lab_records=lab_records)

# Faculty - Study Materials
@app.route('/faculty/study_materials', methods=['GET', 'POST'])
@login_required
def faculty_study_materials():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = StudyMaterialForm()
    form.subject.choices = [(s.id, f"{s.code} - {s.name}") for s in Subject.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            if filename:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'materials', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                form.file.data.save(file_path)
                
                study_material = StudyMaterial(
                    title=form.title.data,
                    description=form.description.data,
                    subject_id=form.subject.data,
                    uploaded_by=current_user.id,
                    file_path=f'uploads/materials/{filename}',
                    file_name=filename,
                    file_size=os.path.getsize(file_path),
                    file_type=filename.split('.')[-1] if '.' in filename else 'unknown'
                )
                db.session.add(study_material)
                db.session.commit()
                flash("Study material uploaded successfully!", "success")
                return redirect(url_for('faculty_study_materials'))
    
    materials = StudyMaterial.query.filter_by(uploaded_by=current_user.id).order_by(StudyMaterial.timestamp.desc()).all()
    return render_template('faculty/study_materials.html', form=form, materials=materials)

# Faculty - View Feedback
@app.route('/faculty/view_feedback')
@login_required
def faculty_view_feedback():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    feedback_records = StudentFeedback.query.filter_by(faculty_id=current_user.id).order_by(StudentFeedback.timestamp.desc()).all()
    return render_template('faculty/view_feedback.html', feedback_records=feedback_records)

# Faculty - View Workload
@app.route('/faculty/view_workload')
@login_required
def view_workload():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    workloads = Workload.query.filter_by(faculty_id=current_user.id).order_by(Workload.timestamp.desc()).all()
    return render_template('faculty/view_workload.html', workloads=workloads)

# Student - Test Marks
@app.route('/student/test_marks')
@login_required
def student_test_marks():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    test_marks = TestMarks.query.filter_by(student_id=current_user.id).order_by(TestMarks.timestamp.desc()).all()
    return render_template('student/test_marks.html', test_marks=test_marks)

# Student - Lab Performance
@app.route('/student/lab_performance')
@login_required
def student_lab_performance():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    lab_records = LabPerformance.query.filter_by(student_id=current_user.id).order_by(LabPerformance.timestamp.desc()).all()
    return render_template('student/lab_performance.html', lab_records=lab_records)

# Student - Study Materials
@app.route('/student/study_materials')
@login_required
def student_study_materials():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    materials = StudyMaterial.query.order_by(StudyMaterial.timestamp.desc()).all()
    return render_template('student/study_materials.html', materials=materials)


# Student - Give Feedback
@app.route('/student_feedback', methods=['GET', 'POST'])
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
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/feedback_form.html', form=form)

# Model Answer Management
@app.route('/hod_dashboard/model_answers', methods=['GET', 'POST'])
@login_required
def manage_model_answers():
    if current_user.role not in ['hod', 'faculty']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ModelAnswerForm()
    
    if form.validate_on_submit():
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            if filename:
                # Create directory if it doesn't exist
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'model_answers')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Add timestamp to filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                
                file_path = os.path.join(upload_dir, filename)
                form.file.data.save(file_path)
                
                model_answer = ModelAnswer(
                    subject_code=form.subject_code.data,
                    subject_name=dict(form.subject_code.choices)[form.subject_code.data],
                    title=form.title.data,
                    description=form.description.data,
                    file_path=f'uploads/model_answers/{filename}',
                    file_type=ext[1:] if ext else 'unknown',
                    uploaded_by=current_user.id,
                    semester=form.semester.data,
                    academic_year=form.academic_year.data
                )
                db.session.add(model_answer)
                db.session.commit()
                flash("Model answer uploaded successfully!", "success")
                return redirect(url_for('manage_model_answers'))
    
    model_answers = ModelAnswer.query.filter_by(is_active=True).order_by(ModelAnswer.timestamp.desc()).all()
    return render_template('hod/model_answers.html', form=form, model_answers=model_answers)

# Student - View Model Answers
@app.route('/student_dashboard/model_answers')
@login_required
def student_model_answers():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    subject_filter = request.args.get('subject', '')
    
    if subject_filter:
        model_answers = ModelAnswer.query.filter_by(subject_code=subject_filter, is_active=True).order_by(ModelAnswer.timestamp.desc()).all()
    else:
        model_answers = ModelAnswer.query.filter_by(is_active=True).order_by(ModelAnswer.timestamp.desc()).all()
    
    # Get unique subjects for filter dropdown
    subjects = [
        ('OOP', 'Object Oriented Programming'),
        ('DMs', 'Discrete Mathematics'),
        ('DTM', 'Database Technology and Management'),
        ('DSU', 'Data Structures'),
        ('AMT', 'Applied Mathematics'),
        ('SET', 'Software Engineering Technology'),
        ('DAN', 'Data Analytics'),
        ('OSY', 'Operating Systems')
    ]
    
    return render_template('student/model_answers.html', 
                         model_answers=model_answers, 
                         subjects=subjects, 
                         current_subject=subject_filter)

# Download Model Answer
@app.route('/download_model_answer/<int:answer_id>')
@login_required
def download_model_answer(answer_id):
    if current_user.role not in ['student', 'faculty', 'hod', 'cc']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    model_answer = ModelAnswer.query.get_or_404(answer_id)
    
    # Increment download count
    model_answer.download_count += 1
    db.session.commit()
    
    file_path = os.path.join('static', model_answer.file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create sample users if they don't exist
        if not User.query.filter_by(username='A.S.Bhatlavande').first():
            hod = User(username='A.S.Bhatlavande', role='hod', full_name='A.S.Bhatlavande', is_active=True)
            hod.set_password('hod123')
            db.session.add(hod)
        
        if not User.query.filter_by(username='cc_user').first():
            cc = User(username='cc_user', role='cc', full_name='CC User', is_active=True)
            cc.set_password('cc123')
            db.session.add(cc)
        
        if not User.query.filter_by(username='faculty_user').first():
            faculty = User(username='faculty_user', role='faculty', full_name='Faculty User', is_active=True)
            faculty.set_password('faculty123')
            db.session.add(faculty)
        
        if not User.query.filter_by(username='student_user').first():
            student = User(username='student_user', role='student', full_name='Student User', is_active=True)
            student.set_password('student123')
            db.session.add(student)
        
        db.session.commit()

# Faculty - Submit Leave Request
@app.route('/faculty_dashboard/submit_leave', methods=['GET', 'POST'])
@login_required
def faculty_submit_leave():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = LeaveRequestForm()
    
    if form.validate_on_submit():
        # Get HOD as approver - use the active HOD with highest ID (most recent)
        hod = User.query.filter_by(role='hod', is_active=True).order_by(User.id.desc()).first()
        print(f"DEBUG: Found HOD user: {hod}")
        if hod:
            print(f"DEBUG: HOD ID: {hod.id}, Username: {hod.username}, Active: {hod.is_active}")
        else:
            # Check all users to see what HOD users exist
            all_hods = User.query.filter_by(role='hod').all()
            print(f"DEBUG: All HOD users in database: {[(h.id, h.username, h.is_active) for h in all_hods]}")
        
        if not hod:
            flash("No HOD found to approve leave request", "error")
            return redirect(url_for('faculty_dashboard'))
        
        leave_request = LeaveRequest(
            user_id=current_user.id,
            approver_id=hod.id,
            leave_type=form.leave_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data
        )
        db.session.add(leave_request)
        db.session.commit()
        print(f"DEBUG: Faculty leave request created - ID: {leave_request.id}, User: {leave_request.user_id}, Approver: {leave_request.approver_id}")
        flash("Leave request submitted successfully!", "success")
        return redirect(url_for('faculty_dashboard'))
    
    return render_template('faculty/submit_leave.html', form=form)

# Student - Submit Leave Request
@app.route('/student_dashboard/submit_leave', methods=['GET', 'POST'])
@login_required
def student_submit_leave():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = LeaveRequestForm()
    
    if form.validate_on_submit():
        # Get CC as approver - use the active CC with highest ID (most recent)
        cc = User.query.filter_by(role='cc', is_active=True).order_by(User.id.desc()).first()
        print(f"DEBUG: Found CC user: {cc}")
        if cc:
            print(f"DEBUG: CC ID: {cc.id}, Username: {cc.username}, Active: {cc.is_active}")
        else:
            # Check all users to see what CC users exist
            all_ccs = User.query.filter_by(role='cc').all()
            print(f"DEBUG: All CC users in database: {[(c.id, c.username, c.is_active) for c in all_ccs]}")
        
        if not cc:
            flash("No CC found to approve leave request", "error")
            return redirect(url_for('student_dashboard'))
        
        leave_request = LeaveRequest(
            user_id=current_user.id,
            approver_id=cc.id,
            leave_type=form.leave_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data
        )
        db.session.add(leave_request)
        db.session.commit()
        print(f"DEBUG: Student leave request created - ID: {leave_request.id}, User: {leave_request.user_id}, Approver: {leave_request.approver_id}")
        flash("Leave request submitted successfully!", "success")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/submit_leave.html', form=form)

# View My Leave Requests (for faculty and students)
@app.route('/my_leave_requests')
@login_required
def my_leave_requests():
    if current_user.role not in ['faculty', 'student']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    leave_requests = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.timestamp.desc()).all()
    
    if current_user.role == 'faculty':
        return render_template('faculty/my_leave_requests.html', leave_requests=leave_requests)
    else:
        return render_template('student/my_leave_requests.html', leave_requests=leave_requests)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
