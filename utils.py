import os
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.utils import secure_filename
from models import User, Workload, Marks, Attendance, Schedule, Report, AuditLog
from extension import db
# Email functionality disabled for now
EMAIL_AVAILABLE = False

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file):
    """Save uploaded profile picture"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f'uploads/profiles/{filename}'
    return None

def calculate_hours_worked(check_in, check_out):
    """Calculate hours worked between check-in and check-out"""
    if check_in and check_out:
        delta = check_out - check_in
        return round(delta.total_seconds() / 3600, 2)
    return 0.0

def get_dashboard_stats(user_role, user_id=None):
    """Get dashboard statistics based on user role"""
    stats = {}
    
    if user_role == 'hod':
        stats['total_faculty'] = User.query.filter_by(role='faculty', is_active=True).count()
        stats['total_students'] = User.query.filter_by(role='student', is_active=True).count()
        stats['total_workloads'] = Workload.query.count()
        # Fix the complaint count query
        from models import Complaint
        stats['pending_complaints'] = Complaint.query.filter_by(status='Pending').count()
        stats['total_subjects'] = db.session.query(Workload.subject).distinct().count()
        
    elif user_role == 'faculty':
        stats['my_workloads'] = Workload.query.filter_by(faculty_id=user_id).count()
        stats['my_schedules'] = Schedule.query.filter_by(faculty_id=user_id).count()
        # Fix the notification count query
        from models import Notification
        stats['unread_notifications'] = Notification.query.filter_by(user_id=user_id, is_read=False).count()
        
    elif user_role == 'student':
        # Fix the complaint count query
        from models import Complaint
        stats['my_complaints'] = Complaint.query.filter_by(student_id=user_id).count()
        stats['my_marks'] = Marks.query.filter_by(student_id=user_id).count()
        
    elif user_role == 'cc':
        # Fix the complaint count queries
        from models import Complaint
        stats['pending_complaints'] = Complaint.query.filter_by(status='Pending').count()
        stats['resolved_complaints'] = Complaint.query.filter_by(status='Resolved').count()
    
    return stats

def generate_workload_report(date_from=None, date_to=None):
    """Generate workload report"""
    query = Workload.query
    if date_from:
        query = query.filter(Workload.timestamp >= date_from)
    if date_to:
        query = query.filter(Workload.timestamp <= date_to)
    
    workloads = query.all()
    
    report_data = []
    for workload in workloads:
        report_data.append({
            'Faculty': workload.faculty.username,
            'Subject': workload.subject,
            'Hours': workload.hours,
            'Assigned Date': workload.timestamp.strftime('%Y-%m-%d'),
            'Assigned By': workload.hod.username if workload.hod else 'N/A'
        })
    
    return report_data

def generate_attendance_report(date_from=None, date_to=None, user_id=None):
    """Generate attendance report"""
    query = Attendance.query
    if date_from:
        query = query.filter(Attendance.date >= date_from)
    if date_to:
        query = query.filter(Attendance.date <= date_to)
    if user_id:
        query = query.filter(Attendance.user_id == user_id)
    
    attendance_records = query.all()
    
    report_data = []
    for record in attendance_records:
        report_data.append({
            'User': record.user.username,
            'Date': record.date.strftime('%Y-%m-%d'),
            'Check In': record.check_in.strftime('%H:%M') if record.check_in else 'N/A',
            'Check Out': record.check_out.strftime('%H:%M') if record.check_out else 'N/A',
            'Status': record.status,
            'Hours Worked': record.hours_worked,
            'Notes': record.notes or ''
        })
    
    return report_data

def export_to_csv(data, filename):
    """Export data to CSV file"""
    if not data:
        return None
    
    export_folder = os.path.join(current_app.root_path, 'static', 'exports')
    os.makedirs(export_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"{filename}_{timestamp}.csv"
    file_path = os.path.join(export_folder, csv_filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    return f'exports/{csv_filename}'

def send_email_notification(to_email, subject, body):
    """Send email notification (currently disabled)"""
    print(f"Email notification would be sent to {to_email}: {subject}")
    return True

def log_user_action(user_id, action, table_name=None, record_id=None, old_values=None, new_values=None, ip_address=None):
    """Log user actions for audit trail"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            ip_address=ip_address
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Audit logging failed: {str(e)}")

def search_records(query, search_type='all'):
    """Search across different record types"""
    results = {
        'users': [],
        'workloads': [],
        'complaints': [],
        'marks': []
    }
    
    if search_type in ['all', 'users']:
        users = User.query.filter(
            db.or_(
                User.username.contains(query),
                User.full_name.contains(query),
                User.email.contains(query)
            )
        ).all()
        results['users'] = users
    
    if search_type in ['all', 'workloads']:
        workloads = Workload.query.filter(
            Workload.subject.contains(query)
        ).all()
        results['workloads'] = workloads
    
    if search_type in ['all', 'marks']:
        marks = Marks.query.filter(
            Marks.subject.contains(query)
        ).all()
        results['marks'] = marks
    
    return results

def get_weekly_schedule(faculty_id):
    """Get weekly schedule for a faculty member"""
    schedules = Schedule.query.filter_by(faculty_id=faculty_id).all()
    
    weekly_schedule = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': []
    }
    
    for schedule in schedules:
        weekly_schedule[schedule.day_of_week].append(schedule)
    
    return weekly_schedule

def calculate_workload_distribution():
    """Calculate workload distribution among faculty"""
    faculty_workloads = db.session.query(
        User.username,
        db.func.sum(Workload.hours).label('total_hours'),
        db.func.count(Workload.id).label('subject_count')
    ).join(Workload, User.id == Workload.faculty_id)\
     .filter(User.role == 'faculty')\
     .group_by(User.id, User.username).all()
    
    return faculty_workloads

def get_marks_analytics():
    """Get marks analytics for dashboard"""
    marks_data = db.session.query(
        Marks.subject,
        db.func.avg(Marks.marks_obtained).label('avg_marks'),
        db.func.count(Marks.id).label('total_entries')
    ).group_by(Marks.subject).all()
    
    return marks_data
