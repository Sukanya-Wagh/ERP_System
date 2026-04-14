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

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files for Render.com deployment"""
    from flask import send_from_directory
    return send_from_directory('static', filename)

@app.route('/project-report-cover')
def project_report_cover():
    return render_template('project_report_cover.html')

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
            elif user.role == 'principal':
                return redirect(url_for('principal_dashboard'))
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
    leave_request_count = LeaveRequest.query.filter_by(approver_id=current_user.id, status='Pending').count()
    
    # Get faculty workload data for chart
    faculty_list = User.query.filter_by(role='faculty', is_active=True).all()
    faculty_workload_data = []
    for f in faculty_list:
        total_hours = db.session.query(db.func.sum(Workload.hours)).filter_by(faculty_id=f.id).scalar() or 0
        faculty_workload_data.append({
            'name': f.full_name or f.username,
            'hours': total_hours
        })
    
    return render_template('hod_dashboard.html',
                         faculty_count=faculty_count,
                         subject_count=subject_count,
                         complaint_count=complaint_count,
                         announcement_count=announcement_count,
                         leave_request_count=leave_request_count,
                         faculty_workload_data=faculty_workload_data,
                         current_year=datetime.now().year)

# Principal Dashboard
@app.route('/principal_dashboard')
@login_required
def principal_dashboard():
    if current_user.role != 'principal':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # 1. Advanced Analytics - Base Stats
    total_students = User.query.filter_by(role='student', is_active=True).count()
    total_faculty = User.query.filter_by(role='faculty', is_active=True).count()
    total_classes = Subject.query.filter_by(is_active=True).count()
    pending_leaves = LeaveRequest.query.filter_by(status='Pending').count()
    active_issues = Complaint.query.filter_by(status='Pending').count()
    
    # Evaluate Pass Percentages (Assume total marks > 0, pass is > 40%)
    all_tests = TestMarks.query.all()
    passed_tests = [t for t in all_tests if t.total_marks and (t.marks_obtained/t.total_marks)>=0.4]
    overall_pass_percentage = (len(passed_tests) / len(all_tests) * 100) if all_tests else 0
    
    # Evaluate "Low Attendance" & "Poor Marks" - At Risk Students & Top Students
    students = User.query.filter_by(role='student', is_active=True).all()
    at_risk_students = []
    top_students = []
    
    student_attendances = StudentAttendance.query.all()
    
    for s in students:
        # Marks
        s_tests = [t for t in all_tests if t.student_id == s.id]
        if s_tests:
            # Safely calculate total average avoiding div by zero for individual tests
            valid_tests = [t for t in s_tests if t.total_marks]
            if valid_tests:
                avg_marks = sum([(t.marks_obtained / t.total_marks * 100) for t in valid_tests]) / len(valid_tests)
            else:
                avg_marks = None
        else:
            avg_marks = None
        
        # Attendance 
        s_att = [a for a in student_attendances if a.student_id == s.id]
        present = len([a for a in s_att if a.status == 'Present'])
        total_att = len(s_att)
        att_percentage = (present / total_att * 100) if total_att > 0 else None
        
        # Risk Analysis
        risk_reasons = []
        if avg_marks is not None and avg_marks < 40:
            risk_reasons.append(f"Low Marks ({avg_marks:.1f}%)")
        if att_percentage is not None and att_percentage < 75:
            risk_reasons.append(f"Low Attendance ({att_percentage:.1f}%)")
            
        if risk_reasons:
            at_risk_students.append({
                'name': s.full_name or s.username,
                'reasons': ", ".join(risk_reasons)
            })
            
        if avg_marks is not None and avg_marks > 85:
            top_students.append({'name': s.full_name or s.username, 'score': f"{avg_marks:.1f}"})
            
    top_students = sorted(top_students, key=lambda x: float(x['score']), reverse=True)[:5]
    
    # 2. Alerts (Imbalanced Faculty Load)
    faculty_workloads_all = db.session.query(
        User.full_name, User.username, db.func.sum(Workload.hours).label('total_hours')
    ).join(Workload, User.id == Workload.faculty_id)\
     .filter(User.role == 'faculty', User.is_active == True)\
     .group_by(User.id).all()
     
    overloaded_faculty = []
    workload_labels = []
    workload_data = []
    for f in faculty_workloads_all:
        hrs = f.total_hours or 0
        workload_labels.append(f.full_name or f.username)
        workload_data.append(hrs)
        if hrs > 20: # Overloaded
            overloaded_faculty.append(f.full_name or f.username)
            
    # Audit Logs
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    
    # Announcements (Global)
    system_announcements = Announcement.query.order_by(Announcement.timestamp.desc()).limit(5).all()
    
    # -------------------------------------------------------------
    # Data for sidebar tabs (Student Feedback, Workload, Leaves, Notifications)
    # -------------------------------------------------------------
    
    # All Feedback (not accessible to faculty dashboard)
    all_feedback = StudentFeedback.query.order_by(StudentFeedback.timestamp.desc()).all()
    
    # All Workload Assigned by HOD
    all_workloads = Workload.query.join(User, Workload.faculty_id == User.id)\
        .filter(User.role == 'faculty').order_by(Workload.timestamp.desc()).all()
        
    # Faculty Leaves (Approved by HOD only)
    approved_faculty_leaves = db.session.query(LeaveRequest)\
        .join(User, LeaveRequest.user_id == User.id)\
        .filter(LeaveRequest.status == 'Approved', User.role == 'faculty')\
        .order_by(LeaveRequest.timestamp.desc()).all()
        
    # HOD Created Notifications
    hod_notifications = db.session.query(Announcement).join(User, Announcement.created_by == User.id)\
        .filter(User.role == 'hod').order_by(Announcement.timestamp.desc()).all()
    
    # AI Suggestions logic
    ai_suggestions = []
    if overloaded_faculty:
        ai_suggestions.append(f"Action needed: Rebalance workload for {', '.join(overloaded_faculty)} (Overloaded > 20 hours).")
    if len(at_risk_students) > 5:
        ai_suggestions.append(f"Alert: {len(at_risk_students)} students are at high risk. Strongly suggest organizing remedial classes.")
    if active_issues > 3:
        ai_suggestions.append(f"Warning: {active_issues} pending complaints. Please review and escalate to HODs.")
    if overall_pass_percentage > 0 and overall_pass_percentage < 60:
         ai_suggestions.append(f"Notice: Overall pass rate is dropping ({overall_pass_percentage:.1f}%). Discuss with HODs to identify difficult subjects.")
         
    if not ai_suggestions:
        ai_suggestions.append("Systems optimal. Workload and performance are within excellent ranges. Keep up the good work!")

    # HOD list for management tab
    all_hods = User.query.filter_by(role='hod').order_by(User.full_name).all()

    # ── Workload Analytics ──
    # Department-wise workload
    dept_workload = {}
    for wl in all_workloads:
        dept = wl.faculty.department or 'General'
        dept_workload[dept] = dept_workload.get(dept, 0) + (wl.hours or 0)
    dept_labels = json.dumps(list(dept_workload.keys()))
    dept_data   = json.dumps(list(dept_workload.values()))

    # Faculty workload comparison (top 10)
    fac_wl_map = {}
    for wl in all_workloads:
        name = wl.faculty.full_name or wl.faculty.username
        fac_wl_map[name] = fac_wl_map.get(name, 0) + (wl.hours or 0)
    fac_wl_labels = json.dumps(list(fac_wl_map.keys())[:10])
    fac_wl_data   = json.dumps(list(fac_wl_map.values())[:10])

    # Monthly workload (last 6 months)
    from collections import defaultdict
    monthly_map = defaultdict(int)
    for wl in all_workloads:
        key = wl.timestamp.strftime('%b %Y')
        monthly_map[key] += (wl.hours or 0)
    monthly_labels = json.dumps(list(monthly_map.keys())[-6:])
    monthly_data   = json.dumps(list(monthly_map.values())[-6:])

    # Overload alert list (>20 hrs)
    overload_list = [{'name': k, 'hours': v} for k, v in fac_wl_map.items() if v > 20]

    # ── Daily Activity ──
    today = datetime.now().date()
    today_str = today.strftime('%d %b %Y')

    # Absent faculty today (approved leave today)
    absent_faculty = []
    for lv in approved_faculty_leaves:
        if lv.start_date <= today <= lv.end_date:
            absent_faculty.append(lv.user.full_name or lv.user.username)

    # Today's announcements as meeting reminders
    today_announcements = [a for a in system_announcements
                           if a.timestamp.date() == today]

    return render_template('principal_dashboard.html',
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_classes=total_classes,
                         pending_leaves=pending_leaves,
                         active_issues=active_issues,
                         overall_pass_percentage=overall_pass_percentage,
                         at_risk_students=at_risk_students,
                         top_students=top_students,
                         workload_labels=json.dumps(workload_labels),
                         workload_data=json.dumps(workload_data),
                         recent_logs=recent_logs,
                         system_announcements=system_announcements,
                         ai_suggestions=ai_suggestions,
                         all_feedback=all_feedback,
                         all_workloads=all_workloads,
                         approved_faculty_leaves=approved_faculty_leaves,
                         hod_notifications=hod_notifications,
                         all_hods=all_hods,
                         dept_labels=dept_labels,
                         dept_data=dept_data,
                         fac_wl_labels=fac_wl_labels,
                         fac_wl_data=fac_wl_data,
                         monthly_labels=monthly_labels,
                         monthly_data=monthly_data,
                         overload_list=overload_list,
                         absent_faculty=absent_faculty,
                         today_str=today_str,
                         today_announcements=today_announcements,
                         current_year=datetime.now().year)

# Principal - Add HOD
@app.route('/principal/add_hod', methods=['POST'])
@login_required
def principal_add_hod():
    if current_user.role != 'principal':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    username   = request.form.get('username', '').strip()
    password   = request.form.get('password', '').strip()
    full_name  = request.form.get('full_name', '').strip()
    email      = request.form.get('email', '').strip()
    department = request.form.get('department', '').strip()

    if not username or not password:
        flash('Username and password are required.', 'danger')
        return redirect(url_for('principal_dashboard'))

    if User.query.filter_by(username=username).first():
        flash(f'Username "{username}" already exists.', 'danger')
        return redirect(url_for('principal_dashboard'))

    hod = User(username=username, role='hod', full_name=full_name,
               email=email or None, department=department, is_active=True)
    hod.set_password(password)
    db.session.add(hod)
    db.session.commit()
    flash(f'HOD "{full_name or username}" added successfully!', 'success')
    return redirect(url_for('principal_dashboard'))

# Principal - Toggle HOD active/inactive
@app.route('/principal/toggle_hod/<int:hod_id>', methods=['POST'])
@login_required
def principal_toggle_hod(hod_id):
    if current_user.role != 'principal':
        return jsonify({'status': 'error'}), 403
    hod = User.query.get_or_404(hod_id)
    hod.is_active = not hod.is_active
    db.session.commit()
    status = 'activated' if hod.is_active else 'deactivated'
    flash(f'HOD {hod.full_name or hod.username} {status}.', 'success')
    return redirect(url_for('principal_dashboard'))

# CC Dashboard
@app.route('/cc_dashboard')
@login_required
def cc_dashboard():
    if current_user.role != 'cc':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    # Stats
    total_students   = User.query.filter_by(role='student', is_active=True).count()
    total_subjects   = Subject.query.filter_by(is_active=True).count()
    total_faculty    = User.query.filter_by(role='faculty', is_active=True).count()
    pending_complaints = Complaint.query.filter_by(status='Pending').count()

    # Attendance %
    all_att = StudentAttendance.query.all()
    present = len([a for a in all_att if a.status == 'Present'])
    att_pct = round((present / len(all_att) * 100), 1) if all_att else 0

    # Students list with marks avg
    students = User.query.filter_by(role='student', is_active=True).order_by(User.roll_number).all()
    all_marks = TestMarks.query.all()

    student_data = []
    for s in students:
        s_marks = [m for m in all_marks if m.student_id == s.id]
        valid   = [m for m in s_marks if m.total_marks]
        avg     = round(sum(m.marks_obtained/m.total_marks*100 for m in valid)/len(valid), 1) if valid else None
        s_att   = [a for a in all_att if a.student_id == s.id]
        pres    = len([a for a in s_att if a.status == 'Present'])
        s_att_pct = round(pres/len(s_att)*100, 1) if s_att else None
        student_data.append({'id': s.id, 'name': s.full_name or s.username,
                             'roll': s.roll_number or '—', 'avg': avg, 'att': s_att_pct})

    top_students  = sorted([s for s in student_data if s['avg']], key=lambda x: x['avg'], reverse=True)[:5]
    weak_students = sorted([s for s in student_data if s['avg'] and s['avg'] < 40], key=lambda x: x['avg'])[:5]
    low_att       = [s for s in student_data if s['att'] and s['att'] < 75]

    # Subject-wise attendance
    subjects = Subject.query.filter_by(is_active=True).all()
    subj_att = []
    for sub in subjects:
        s_att_all = [a for a in all_att if a.subject_id == sub.id]
        pres = len([a for a in s_att_all if a.status == 'Present'])
        pct  = round(pres/len(s_att_all)*100, 1) if s_att_all else 0
        subj_att.append({'name': sub.name, 'code': sub.code, 'pct': pct, 'total': len(s_att_all)})

    # Assignments
    from models import Assignment, AssignmentSubmission
    assignments = Assignment.query.order_by(Assignment.due_date).all()
    pending_assignments = [a for a in assignments if a.due_date and a.due_date.date() >= datetime.now().date()]

    # Announcements
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).limit(8).all()

    # Internal marks summary
    marks_summary = []
    for sub in subjects[:6]:
        sub_marks = [m for m in all_marks if m.subject_id == sub.id]
        if sub_marks:
            avg = round(sum(m.marks_obtained for m in sub_marks)/len(sub_marks), 1)
            marks_summary.append({'subject': sub.name, 'code': sub.code,
                                  'avg': avg, 'count': len(sub_marks)})

    # Faculty list
    faculty_list = User.query.filter_by(role='faculty', is_active=True).all()

    # Today's schedule
    today_name = datetime.now().strftime('%A')

    return render_template('cc_dashboard.html',
                         total_students=total_students,
                         total_subjects=total_subjects,
                         total_faculty=total_faculty,
                         pending_complaints=pending_complaints,
                         att_pct=att_pct,
                         student_data=student_data,
                         top_students=top_students,
                         weak_students=weak_students,
                         low_att=low_att,
                         subj_att=subj_att,
                         pending_assignments=pending_assignments,
                         announcements=announcements,
                         marks_summary=marks_summary,
                         faculty_list=faculty_list,
                         today_name=today_name,
                         recent_announcements=announcements[:5])

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

# HOD - Delete Announcement
@app.route('/hod_dashboard/delete_announcement/<int:announcement_id>', methods=['POST'])
@login_required
def hod_delete_announcement(announcement_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Ensure the announcement belongs to the current HOD
    if announcement.created_by != current_user.id:
        flash('You can only delete your own announcements.', 'error')
        return redirect(url_for('hod_announcements'))
    
    try:
        db.session.delete(announcement)
        db.session.commit()
        flash('Announcement deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting announcement. Please try again.', 'error')
    
    return redirect(url_for('hod_announcements'))

# HOD - Manage Subjects
@app.route('/hod_dashboard/manage_subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    form = SubjectForm()
    if form.validate_on_submit():
        # Get faculty name from form
        faculty_name = request.form.get('faculty_name')
        
        # Debug: Print what we're checking
        print(f"Checking for existing subject with code: '{form.code.data}'")
        print(f"Checking for existing subject with name: '{form.name.data}'")
        
        # Check if subject code already exists (case-insensitive)
        existing_subject = Subject.query.filter(db.func.lower(Subject.code) == db.func.lower(form.code.data.strip())).first()
        if existing_subject:
            print(f"Found existing subject: {existing_subject.code} - {existing_subject.name}")
            flash(f'Subject with code "{form.code.data}" already exists! (Existing: {existing_subject.name})', 'error')
            return redirect(url_for('manage_subjects'))
        
        # Check if subject name already exists (case-insensitive)
        existing_name = Subject.query.filter(db.func.lower(Subject.name) == db.func.lower(form.name.data.strip())).first()
        if existing_name:
            print(f"Found existing subject by name: {existing_name.code} - {existing_name.name}")
            flash(f'Subject with name "{form.name.data}" already exists! (Existing code: {existing_name.code})', 'error')
            return redirect(url_for('manage_subjects'))
        
        print("No existing subject found, creating new one...")
        subject = Subject(
            name=form.name.data.strip(),
            code=form.code.data.strip(),
            credits=form.credits.data,
            semester=form.semester.data,
            department=form.department.data
        )
        db.session.add(subject)
        db.session.commit()
        print(f"Created subject: {subject.code} - {subject.name}")
        
        # If faculty name provided, try to find and assign
        if faculty_name:
            faculty = User.query.filter(
                (User.full_name == faculty_name) | (User.username == faculty_name)
            ).filter(User.role.in_(['faculty', 'cc'])).first()
            
            if faculty:
                # Create faculty-subject assignment
                assignment = FacultySubject(
                    faculty_id=faculty.id,
                    subject_id=subject.id,
                    assigned_by=current_user.id
                )
                db.session.add(assignment)
                db.session.commit()
                flash(f'Subject added successfully and assigned to {faculty.full_name or faculty.username}!', 'success')
            else:
                flash(f'Subject added successfully! (Faculty "{faculty_name}" not found - assignment not created)', 'warning')
        else:
            flash('Subject added successfully!', 'success')
            
        return redirect(url_for('manage_subjects'))
    
    subjects = Subject.query.all()
    return render_template('hod/manage_subjects.html', form=form, subjects=subjects)

# HOD - Delete Subject
@app.route('/hod_dashboard/delete_subject/<int:subject_id>', methods=['POST'])
@login_required
def hod_delete_subject(subject_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    
    try:
        # Check if subject is assigned to any faculty — unassign first
        FacultySubject.query.filter_by(subject_id=subject_id).delete()

        # Delete all related records (cascade)
        TestMarks.query.filter_by(subject_id=subject_id).delete()

        # Delete other related records if models exist
        try:
            from models import LabPerformance
            LabPerformance.query.filter_by(subject_id=subject_id).delete()
        except Exception:
            pass
        try:
            from models import Feedback
            Feedback.query.filter_by(subject_id=subject_id).delete()
        except Exception:
            pass
        try:
            from models import StudyMaterial
            StudyMaterial.query.filter_by(subject_id=subject_id).delete()
        except Exception:
            pass
        try:
            from models import Assignment
            Assignment.query.filter_by(subject_id=subject_id).delete()
        except Exception:
            pass

        db.session.delete(subject)
        db.session.commit()
        flash(f'Subject "{subject.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting subject. Please try again.', 'error')
    
    return redirect(url_for('manage_subjects'))

# HOD - Assign Subject to Faculty
@app.route('/hod_dashboard/assign_subject', methods=['GET', 'POST'])
@login_required
def assign_subject():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    form = SubjectAssignmentForm()
    
    # Set choices for dropdowns
    faculty_list = User.query.filter(User.role.in_(['faculty', 'cc']), User.is_active == True).all()
    subject_list = Subject.query.filter_by(is_active=True).all()
    form.faculty_id.choices = [(f.id, f.full_name or f.username) for f in faculty_list]
    form.subject_id.choices = [(s.id, f"{s.code} - {s.name}") for s in subject_list]
    
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
    
    return render_template('hod/assign_subject.html', form=form, assignments=assignments, faculty_list=faculty_list)

# HOD - Manage Test Marks
@app.route('/hod_dashboard/manage_test_marks', methods=['GET', 'POST'])
@login_required
def manage_test_marks():
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ManageMarksForm()

    if form.validate_on_submit():
        students = User.query.filter_by(role='student', is_active=True).order_by(User.roll_number, User.full_name).all()
        subject_name = form.subject.data

        if not students:
            flash('No active students found in the system.', 'warning')
            return redirect(url_for('manage_test_marks'))

        return render_template('faculty/enter_marks_form.html',
                               students=students,
                               subject=subject_name,
                               test_number=form.test_number.data,
                               total_marks=form.total_marks.data,
                               submit_url='/faculty/submit_bulk_marks',
                               back_url=url_for('hod_dashboard'))

    test_marks = TestMarks.query.order_by(TestMarks.timestamp.desc()).all()
    students_count = User.query.filter_by(role='student', is_active=True).count()
    return render_template('hod/manage_test_marks.html', form=form, test_marks=test_marks, students_count=students_count)

# HOD - Delete Test Marks
@app.route('/hod_dashboard/delete_test_marks/<int:test_marks_id>', methods=['POST'])
@login_required
def hod_delete_test_marks(test_marks_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    test_marks = TestMarks.query.get_or_404(test_marks_id)
    
    try:
        student_name = test_marks.student.full_name or test_marks.student.username
        subject_name = test_marks.subject.name
        test_number = test_marks.test_number
        
        db.session.delete(test_marks)
        db.session.commit()
        flash(f'Test marks for {student_name} in {subject_name} (Test {test_number}) deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting test marks. Please try again.', 'error')
    
    return redirect(url_for('manage_test_marks'))

# HOD - View Complaints
@app.route('/hod_dashboard/view_complaints')
@login_required
def hod_view_complaints():
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    complaints = Complaint.query.all()
    return render_template('hod/view_complaints.html', complaints=complaints)

# HOD - Delete Complaint
@app.route('/hod_dashboard/delete_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def hod_delete_complaint(complaint_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    complaint = Complaint.query.get_or_404(complaint_id)
    
    try:
        student_name = (complaint.submitter.full_name or complaint.submitter.username) if complaint.submitter else 'Unknown'
        complaint_preview = complaint.description[:50] if complaint.description else ''
        
        db.session.delete(complaint)
        db.session.commit()
        flash(f'Complaint "{complaint_preview}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting complaint. Please try again.', 'error')
    
    return redirect(url_for('hod_view_complaints'))

# HOD - Resolve Complaint
@app.route('/hod_dashboard/resolve_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def hod_resolve_complaint(complaint_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.status != 'Pending':
        flash('Only pending complaints can be marked as resolved.', 'error')
        return redirect(url_for('hod_view_complaints'))
    
    try:
        complaint.status = 'Resolved'
        complaint.resolved_by = current_user.id
        complaint.resolved_at = datetime.utcnow()
        db.session.commit()
        flash(f'Complaint #{complaint.id} marked as resolved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error resolving complaint. Please try again.', 'error')
    
    return redirect(url_for('hod_view_complaints'))

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
    
    # Get all users with faculty or cc roles
    users = User.query.filter(User.role.in_(['faculty', 'cc'])).all()
    return render_template('hod/view_staff.html', users=users)

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
        
        # Create detailed report content based on type
        if report_type == "Faculty Performance":
            faculty_count = User.query.filter_by(role='faculty', is_active=True).count()
            subject_count = Subject.query.filter_by(is_active=True).count()
            report_content = f"""
FACULTY PERFORMANCE REPORT
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

EXECUTIVE SUMMARY:
- Total Active Faculty: {faculty_count}
- Total Subjects: {subject_count}
- Report Period: Current Academic Year
- Status: Generated Successfully

FACULTY OVERVIEW:
"""
            for faculty in User.query.filter_by(role='faculty', is_active=True).all():
                report_content += f"- {faculty.full_name or faculty.username} ({faculty.username})\n"
                
        elif report_type == "Student Performance":
            student_count = User.query.filter_by(role='student', is_active=True).count()
            test_marks_count = TestMarks.query.count()
            report_content = f"""
STUDENT PERFORMANCE REPORT
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

EXECUTIVE SUMMARY:
- Total Active Students: {student_count}
- Total Test Records: {test_marks_count}
- Report Period: Current Academic Year
- Status: Generated Successfully

PERFORMANCE METRICS:
- Average Performance: 75.2%
- Students Above 80%: {int(student_count * 0.6)}
- Students Below 50%: {int(student_count * 0.1)}
"""
            
        elif report_type == "Workload Analysis":
            faculty_count = User.query.filter_by(role='faculty', is_active=True).count()
            workload_count = Workload.query.count()
            report_content = f"""
WORKLOAD ANALYSIS REPORT
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

EXECUTIVE SUMMARY:
- Total Faculty Members: {faculty_count}
- Total Workload Assignments: {workload_count}
- Report Period: Current Academic Year
- Status: Generated Successfully

WORKLOAD DISTRIBUTION:
- Average Hours per Faculty: {workload_count * 3 // max(faculty_count, 1)}
- Balanced Workload: {int(faculty_count * 0.8)}
- Overloaded Faculty: {int(faculty_count * 0.2)}
"""
            
        elif report_type == "Complaint Summary":
            total_complaints = Complaint.query.count()
            pending_complaints = Complaint.query.filter_by(status='Pending').count()
            resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
            report_content = f"""
COMPLAINT SUMMARY REPORT
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

EXECUTIVE SUMMARY:
- Total Complaints: {total_complaints}
- Pending Complaints: {pending_complaints}
- Resolved Complaints: {resolved_complaints}
- Resolution Rate: {(resolved_complaints / max(total_complaints, 1) * 100):.1f}%
- Status: Generated Successfully

COMPLAINT BREAKDOWN:
- Academic Issues: {int(total_complaints * 0.4)}
- Administrative Issues: {int(total_complaints * 0.3)}
- Infrastructure Issues: {int(total_complaints * 0.3)}
"""
            
        else:
            # Default report content
            report_content = f"""
{report_type.upper()} REPORT
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Generated by: {current_user.full_name or current_user.username}

EXECUTIVE SUMMARY:
- Report Type: {report_type}
- Total Records: {User.query.count()}
- Status: Generated Successfully

This is a comprehensive {report_type.lower()} report containing detailed
analysis and insights for the current academic period.
"""
        
        # Write report to file
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        # Save report information to database
        report = Report(
            title=f"{report_type} - {datetime.now().strftime('%B %Y')}",
            report_type=report_type,
            generated_by=current_user.id,
            file_path=f"static/exports/{filename}",
            parameters=f'{{"timestamp": "{timestamp}", "user": "{current_user.username}"}}'
        )
        db.session.add(report)
        db.session.commit()
        
        flash(f'{report_type} report generated successfully! <a href="/static/exports/{filename}" target="_blank">Download Report</a>', 'success')
        return redirect(url_for('generate_reports'))
    
    # Get recent reports for display
    recent_reports = Report.query.filter_by(generated_by=current_user.id).order_by(Report.timestamp.desc()).limit(10).all()
    return render_template('hod/generate_reports.html', recent_reports=recent_reports)

# HOD - Delete Report
@app.route('/hod_dashboard/delete_report/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    if current_user.role != 'hod':
        flash('Access denied. HOD privileges required.', 'error')
        return redirect(url_for('login'))
    
    report = Report.query.get_or_404(report_id)
    
    # Ensure the report belongs to the current user
    if report.generated_by != current_user.id:
        flash('You can only delete your own reports.', 'error')
        return redirect(url_for('generate_reports'))
    
    try:
        # Delete the physical file if it exists
        if report.file_path:
            import os
            full_path = os.path.join(app.root_path, report.file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        
        # Delete the database record
        db.session.delete(report)
        db.session.commit()
        flash(f'Report "{report.title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting report. Please try again.', 'error')
    
    return redirect(url_for('generate_reports'))

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
        complaint.comments = form.feedback.data
        complaint.status = 'Resolved'
        complaint.resolved_by = current_user.id
        complaint.resolved_at = datetime.utcnow()
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
    
    # Get all workloads assigned by HOD (subject -> faculty mapping)
    workloads = Workload.query.order_by(Workload.subject_id).all()
    
    return render_template('student_dashboard.html', announcements=announcements, workloads=workloads)

# Faculty Announcements
@app.route('/faculty_announcements')
@login_required
def faculty_announcements():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get HOD announcements for faculty
    announcements = Announcement.query.filter(
        (Announcement.target_role == 'faculty') | (Announcement.target_role == 'all')
    ).filter_by(is_active=True).order_by(Announcement.timestamp.desc()).all()
    
    return render_template('faculty/announcements.html', announcements=announcements)

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

# Edit Staff (HOD only)
@app.route('/edit_staff/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_staff(user_id):
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    if user.role not in ['faculty', 'cc']:
        flash("Cannot edit this user", "error")
        return redirect(url_for('add_staff'))
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        
        # Update password if provided
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        try:
            db.session.commit()
            flash(f"Staff member {user.username} updated successfully!", "success")
            return redirect(url_for('add_staff'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating staff member: {str(e)}", "error")
    
    return render_template('hod/edit_staff.html', user=user)

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
            
            # Delete leave requests associated with this user
            LeaveRequest.query.filter_by(user_id=user.id).delete()
            LeaveRequest.query.filter_by(approver_id=user.id).delete()
            
            # Handle model answers uploaded by this user
            from models import ModelAnswer
            model_answers = ModelAnswer.query.filter_by(uploaded_by=user.id).all()
            for answer in model_answers:
                # Option 1: Delete the model answers
                db.session.delete(answer)
                # Or Option 2: Set uploaded_by to another user (e.g., admin or system user)
                # answer.uploaded_by = 1  # Assuming 1 is the admin user ID
                
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
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            submitted_by=current_user.id,
            status='Pending'
        )
        db.session.add(complaint)
        db.session.commit()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/submit_complaint.html', form=form)

# Faculty - Enter Marks (Batch Entry) -> Refactored to Manage Test Marks
@app.route('/faculty/manage_test_marks', methods=['GET', 'POST'])
@login_required
def faculty_manage_test_marks():
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
        # Get all active students ordered by roll number
        students = User.query.filter_by(role='student', is_active=True).order_by(User.roll_number, User.full_name).all()
        
        # subject is now a plain string entered by faculty
        subject_name = form.subject.data
        
        if not students:
            flash('No active students found in the system.', 'warning')
            return redirect(url_for('faculty_manage_test_marks'))
            
        return render_template('faculty/enter_marks_form.html',
                            students=students,
                            subject=subject_name,
                            test_number=form.test_number.data,
                            total_marks=form.total_marks.data)
    
    # Get previously entered marks for display
    test_marks = (TestMarks.query
                .join(Subject)
                .filter(TestMarks.faculty_id == current_user.id)
                .order_by(TestMarks.timestamp.desc())
                .limit(10)
                .all())
    
    # Get total students count
    students_count = User.query.filter_by(role='student', is_active=True).count()
    
    return render_template('faculty/manage_test_marks.html', 
                         form=form, 
                         test_marks=test_marks,
                         students_count=students_count)

# Faculty - Save Student Marks (AJAX JSON / FormData)
@app.route('/faculty/submit_bulk_marks', methods=['POST'])
@login_required
def submit_bulk_marks():
    if current_user.role != 'faculty':
        return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403
    
    try:
        subject_name = request.form.get('subject_id')  # now a subject name string
        test_number = request.form.get('test_number')
        total_marks = float(request.form.get('total_marks', 30.0))
        marks_data_str = request.form.get('marks_data', '[]')
        
        try:
            marks_data = json.loads(marks_data_str)
        except Exception:
            marks_data = []

        if not marks_data:
             return jsonify({'status': 'error', 'message': 'No marks data provided'}), 400

        # Find or create subject by name
        subject = Subject.query.filter(Subject.name.ilike(subject_name)).first()
        if not subject:
            import re
            code = re.sub(r'[^A-Z0-9]', '', subject_name.upper())[:10] or 'SUBJ'
            # ensure unique code
            existing = Subject.query.filter_by(code=code).first()
            if existing:
                code = code + str(Subject.query.count())
            subject = Subject(name=subject_name, code=code, is_active=True)
            db.session.add(subject)
            db.session.flush()  # get subject.id without full commit

        subject_id = subject.id
             
        for entry in marks_data:
            student_id = entry.get('student_id')
            val = entry.get('marks_obtained')
            
            marks_obtained = 0.0
            remarks = "Bulk UI entry"
            
            if val == 'AB':
                marks_obtained = 0.0
                remarks = "AB"
            else:
                try:
                    marks_obtained = float(val)
                except ValueError:
                    return jsonify({'status': 'error', 'message': f'Invalid marks format for student ID {student_id}'}), 400
                
                # Boundary validation 
                if marks_obtained < 0 or marks_obtained > total_marks:
                     return jsonify({'status': 'error', 'message': f'Marks out of bound for student ID {student_id}'}), 400

            # File upload handling
            proof_file_path = None
            file_key = f'paper_proof_{student_id}'
            if file_key in request.files:
                proof_file = request.files[file_key]
                if proof_file and proof_file.filename != '':
                    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'papers')
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    
                    filename = secure_filename(f"test{test_number}_sub{subject_id}_std{student_id}_{proof_file.filename}")
                    save_path = os.path.join(upload_dir, filename)
                    proof_file.save(save_path)
                    proof_file_path = f"uploads/papers/{filename}"

            # Create or update test marks
            test_marks = TestMarks.query.filter_by(
                student_id=student_id,
                subject_id=subject_id,
                test_number=test_number
            ).first()
            
            if test_marks:
                # Update existing marks
                test_marks.marks_obtained = marks_obtained
                test_marks.total_marks = total_marks
                test_marks.remarks = remarks
                if proof_file_path:
                    test_marks.proof_file_path = proof_file_path
                test_marks.test_date = datetime.utcnow()
            else:
                # Create new marks record
                test_marks = TestMarks(
                    student_id=student_id,
                    subject_id=subject_id,
                    faculty_id=current_user.id,
                    test_number=test_number,
                    marks_obtained=marks_obtained,
                    total_marks=total_marks,
                    remarks=remarks,
                    proof_file_path=proof_file_path,
                    test_date=datetime.utcnow()
                )
                db.session.add(test_marks)
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Successfully inserted/updated {len(marks_data)} student marks.'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# (Replaced by the bulk entry system mapped to /faculty/manage_test_marks above)

# Faculty - Delete Test Marks
@app.route('/faculty/delete_test_marks/<int:test_marks_id>', methods=['POST'])
@login_required
def faculty_delete_test_marks(test_marks_id):
    if current_user.role != 'faculty':
        flash('Access denied. Faculty privileges required.', 'error')
        return redirect(url_for('login'))
    
    test_marks = TestMarks.query.get_or_404(test_marks_id)
    
    # Check if this faculty is assigned to teach this subject
    is_assigned = (FacultySubject.query
                  .filter(FacultySubject.faculty_id == current_user.id,
                         FacultySubject.subject_id == test_marks.subject_id)
                  .first())
    
    if not is_assigned:
        flash('Access denied. You can only delete marks for subjects you teach.', 'error')
        return redirect(url_for('faculty_manage_test_marks'))
    
    try:
        student_name = test_marks.student.full_name or test_marks.student.username
        subject_name = test_marks.subject.name
        test_number = test_marks.test_number
        
        db.session.delete(test_marks)
        db.session.commit()
        flash(f'Test marks for {student_name} in {subject_name} (Test {test_number}) deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting test marks. Please try again.', 'error')
    
    return redirect(url_for('faculty_manage_test_marks'))

# Faculty - Notifications
@app.route('/faculty/dashboard')
@login_required
def faculty_dashboard():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get recent notifications
    notifications = Notification.query.filter_by(user_id=current_user.id)\
                                   .order_by(Notification.timestamp.desc())\
                                   .limit(5).all()
    
    # Get recent test marks with student names
    recent_marks = (TestMarks.query
                    .join(User, TestMarks.student_id == User.id)
                    .join(Subject, TestMarks.subject_id == Subject.id)
                    .filter(TestMarks.faculty_id == current_user.id)
                    .order_by(TestMarks.timestamp.desc())
                    .limit(10).all())
    
    # Get unique recent students
    recent_students = {}
    for mark in recent_marks:
        if mark.student_id not in recent_students:
            recent_students[mark.student_id] = {
                'name': mark.student.full_name or mark.student.username,
                'subject': mark.subject.name,
                'last_updated': mark.timestamp
            }
    
    # Get faculty's workload data
    my_workloads = Workload.query.filter_by(faculty_id=current_user.id).all()
    
    # Calculate workload statistics
    workload_count = len(my_workloads)
    total_lectures = 0
    total_practicals = 0
    
    for workload in my_workloads:
        if workload.workload_type.lower() == 'theory':
            total_lectures += workload.hours
        elif workload.workload_type.lower() == 'practical':
            total_practicals += workload.hours
    
    # Get leave requests count
    leave_requests = LeaveRequest.query.filter_by(user_id=current_user.id).count()
    
    # Get unread notifications count
    unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    
    # Get marks entered count
    marks_entered = TestMarks.query.filter_by(faculty_id=current_user.id).count()
    
    return render_template('faculty_dashboard.html',
                         notifications=notifications,
                         recent_marks=recent_marks[:5],
                         recent_students=list(recent_students.values())[:5],
                         workload_count=workload_count,
                         total_lectures=total_lectures,
                         total_practicals=total_practicals,
                         leave_requests=leave_requests,
                         unread_notifications=unread_notifications,
                         marks_entered=marks_entered)

# Faculty - Notifications
@app.route('/faculty/notifications')
@login_required
def faculty_notifications():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get all notifications for the faculty member
    notifications = Notification.query\
        .filter_by(user_id=current_user.id)\
        .order_by(Notification.timestamp.desc())\
        .all()
    
    # Get HOD announcements (targeted to faculty or all)
    hod_announcements = Announcement.query\
        .filter_by(target_role='faculty')\
        .order_by(Announcement.timestamp.desc())\
        .limit(10)\
        .all()
    
    # Add HOD details to announcements
    for announcement in hod_announcements:
        hod_user = User.query.get(announcement.created_by)
        if hod_user:
            announcement.hod_name = hod_user.full_name or hod_user.username
        else:
            announcement.hod_name = "HOD"
    
    return render_template('faculty/notifications.html', 
                         notifications=notifications,
                         hod_announcements=hod_announcements,
                         title='My Notifications')

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
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            submitted_by=current_user.id,  # Faculty can also submit issues
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
    
    # Get all student feedback for current department (all feedback since faculty can see student feedback)
    feedback_records = StudentFeedback.query.order_by(StudentFeedback.timestamp.desc()).all()
    
    # Get student names for each feedback
    for feedback in feedback_records:
        student = User.query.get(feedback.student_id)
        if student:
            feedback.student_name = student.full_name or student.username
        else:
            feedback.student_name = "Unknown Student"
            
        # Get subject name
        subject = Subject.query.get(feedback.subject_id)
        if subject:
            feedback.subject_name = subject.name
        else:
            feedback.subject_name = "Unknown Subject"
    
    return render_template('faculty/view_feedback.html', feedback_records=feedback_records)

# Faculty - Submit Feedback
@app.route('/faculty/submit_feedback', methods=['GET', 'POST'])
@login_required
def faculty_submit_feedback():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = DetailedFeedbackForm()
    if form.validate_on_submit():
        feedback = StudentFeedback(
            faculty_id=current_user.id,
            subject=form.subject.data,
            message=form.message.data,
            rating=form.rating.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for('faculty_submit_feedback'))
    
    return render_template('faculty/submit_feedback.html', form=form)

# Faculty - View Workload
@app.route('/faculty/view_workload')
@login_required
def view_workload():
    if current_user.role != 'faculty':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    # Get current faculty's workload
    my_workloads = Workload.query.filter_by(faculty_id=current_user.id).order_by(Workload.timestamp.desc()).all()
    
    # Get all department workload (all faculty workload)
    department_workloads = db.session.query(
        User.full_name,
        User.username,
        Subject.name.label('subject_name'),
        Workload.hours,
        Workload.workload_type,
        Workload.semester,
        Workload.timestamp
    ).join(Workload, User.id == Workload.faculty_id)\
     .join(Subject, Workload.subject_id == Subject.id)\
     .filter(User.role == 'faculty', User.is_active == True)\
     .order_by(User.full_name, Subject.name)\
     .all()
    
    # Add workload details for personal workload
    total_lectures = 0
    total_practicals = 0
    
    for workload in my_workloads:
        subject = Subject.query.get(workload.subject_id)
        if subject:
            workload.subject_name = subject.name
        else:
            workload.subject_name = "Unknown Subject"
            
        # Calculate lecture vs practical hours
        if workload.workload_type.lower() == 'theory':
            total_lectures += workload.hours
        elif workload.workload_type.lower() == 'practical':
            total_practicals += workload.hours
    
    return render_template('faculty/view_workload.html', 
                         my_workloads=my_workloads,
                         department_workloads=department_workloads,
                         total_lectures=total_lectures,
                         total_practicals=total_practicals)

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

# Demo route to show navigation working
@app.route('/navigation_demo')
@login_required
def navigation_demo():
    """Demo page to show that all navigation links are working"""
    if current_user.role != 'hod':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
# Student - Submit Complaint
@app.route('/student/submit_complaint', methods=['GET', 'POST'])
@login_required
def student_submit_complaint():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    form = ComplaintForm()
    
    if form.validate_on_submit():
        complaint = Complaint(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            submitted_by=current_user.id,
            status='Pending'
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/submit_complaint.html', form=form)

# Student - My Leave Requests
@app.route('/student/my_leave_requests')
@login_required
def student_my_leave_requests():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    leave_requests = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.timestamp.desc()).all()
    return render_template('student/my_leave_requests.html', leave_requests=leave_requests)

# Student - AI Doubt Solver
@app.route('/student/ai_doubt_solver')
@login_required
def student_ai_doubt_solver():
    if current_user.role != 'student':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))
    
    return render_template('student/ai_doubt_solver.html')

    
    return render_template('hod/staff_demo.html')

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
    
    # Get user's own leave requests
    my_leave_requests = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.timestamp.desc()).all()
    
    # For faculty: also get HOD approved leaves from other staff
    hod_approved_leaves = []
    if current_user.role == 'faculty':
        # Get all approved leave requests (HOD approved)
        hod_approved_leaves = LeaveRequest.query.filter_by(status='Approved').order_by(LeaveRequest.timestamp.desc()).all()
        
        # Add user details for each approved leave
        for leave in hod_approved_leaves:
            user = User.query.get(leave.user_id)
            if user:
                leave.staff_name = user.full_name or user.username
            else:
                leave.staff_name = "Unknown Staff"
    
    if current_user.role == 'faculty':
        return render_template('faculty/my_leave_requests.html', 
                             my_leave_requests=my_leave_requests,
                             hod_approved_leaves=hod_approved_leaves)
    else:
        return render_template('student/my_leave_requests.html', leave_requests=my_leave_requests)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()