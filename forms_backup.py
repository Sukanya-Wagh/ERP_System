from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField, FloatField, DateField, TimeField, FileField, BooleanField, PasswordField, DateTimeField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, Regexp
from flask_wtf.file import FileAllowed
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ComplaintForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200), Regexp(r'^[A-Za-z0-9\s\-\'\.\,!?]+$', message='Title can only contain letters, numbers, spaces, and basic punctuation')])
    category = SelectField('Category', choices=[
        ('academic', 'Academic'),
        ('infrastructure', 'Infrastructure'),
        ('faculty', 'Faculty'),
        ('administration', 'Administration'),
        ('hostel', 'Hostel'),
        ('transport', 'Transport'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Complaint')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Feedback')

class WorkloadForm(FlaskForm):
    faculty = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=150)])
    hours = IntegerField('Hours', validators=[DataRequired(), NumberRange(min=1, max=40)])
    submit = SubmitField('Assign Workload')

class MarksForm(FlaskForm):
    student = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    marks_obtained = FloatField('Marks Obtained', validators=[DataRequired()])
    total_marks = FloatField('Total Marks', validators=[DataRequired()])
    submit = SubmitField('Send Marks')

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(), 
        Length(min=2, max=200),
        Regexp(r'^[A-Za-z\s\-\'\.]+$', message='Name can only contain letters, spaces, hyphens, apostrophes, and periods')
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[
        Optional(), 
        Length(max=15),
        Regexp(r'^[\d\s\-\+\(\)]+$', message='Phone number can only contain digits, spaces, hyphens, plus, and parentheses')
    ])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')

class AttendanceForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    check_in = TimeField('Check In Time', validators=[Optional()])
    check_out = TimeField('Check Out Time', validators=[Optional()])
    status = SelectField('Status', choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late'), ('Half-day', 'Half-day')], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Record Attendance')

class ScheduleForm(FlaskForm):
    faculty = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=150)])
    day_of_week = SelectField('Day of Week', choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')
    ], validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    room_number = StringField('Room Number', validators=[Optional(), Length(max=50)])
    semester = StringField('Semester', validators=[Optional(), Length(max=20)])
    academic_year = StringField('Academic Year', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Create Schedule')

class ReportForm(FlaskForm):
    title = StringField('Report Title', validators=[DataRequired(), Length(min=5, max=200)])
    report_type = SelectField('Report Type', choices=[
        ('workload', 'Workload Report'),
        ('attendance', 'Attendance Report'),
        ('marks', 'Marks Report'),
        ('user_activity', 'User Activity Report')
    ], validators=[DataRequired()])
    date_from = DateField('From Date', validators=[Optional()])
    date_to = DateField('To Date', validators=[Optional()])
    submit = SubmitField('Generate Report')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=1, max=200)])
    search_type = SelectField('Search In', choices=[
        ('all', 'All'),
        ('users', 'Users'),
        ('workloads', 'Workloads'),
        ('complaints', 'Complaints'),
        ('marks', 'Marks')
    ], default='all')
    submit = SubmitField('Search')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class SystemSettingsForm(FlaskForm):
    setting_key = StringField('Setting Key', validators=[DataRequired(), Length(max=100)])
    setting_value = TextAreaField('Setting Value', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Update Setting')


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200), Regexp(r'^[A-Za-z0-9\s\-\'\.\,\!]+$', message='Title can only contain letters, numbers, spaces, and basic punctuation')])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    target_role = SelectField('Target Audience', choices=[
        ('faculty', 'Faculty'),
        ('student', 'Students'),
        ('all', 'All Users')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low')
    ], default='normal')
    expires_at = DateField('Expires On', validators=[Optional()])
    submit = SubmitField('Create Announcement')


class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=150), Regexp(r'^[A-Za-z0-9\s\-\'\.&]+$', message='Subject name can only contain letters, numbers, spaces, hyphens, apostrophes, periods, and ampersands')])
    code = StringField('Subject Code', validators=[DataRequired(), Length(min=2, max=20), Regexp(r'^[A-Za-z0-9\-_]+$', message='Subject code can only contain letters, numbers, hyphens, and underscores')])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    semester = StringField('Semester', validators=[Optional(), Length(max=20)])
    credits = IntegerField('Credits', validators=[Optional(), NumberRange(min=1, max=10)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Add Subject')


class AssignSubjectForm(FlaskForm):
    faculty = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired(), Length(max=20)])
    semester = SelectField('Semester', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Subject')

class SubjectAssignmentForm(FlaskForm):
    faculty_id = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired(), Length(max=20)])
    semester = SelectField('Semester', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Subject')


class TestMarksForm(FlaskForm):
    student = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    test_number = SelectField('Test Number', choices=[
        (1, 'Test 1'), (2, 'Test 2'), (3, 'Test 3'), (4, 'Test 4'), (5, 'Test 5')
    ], coerce=int, validators=[DataRequired()])
    marks_obtained = FloatField('Marks Obtained', validators=[DataRequired(), NumberRange(min=0)])
    total_marks = FloatField('Total Marks', validators=[DataRequired(), NumberRange(min=1)])
    test_date = DateField('Test Date', validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Add Marks')


class LabPerformanceForm(FlaskForm):
    student = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    lab_session = StringField('Lab Session', validators=[DataRequired(), Length(min=2, max=100)])
    performance_score = FloatField('Performance Score (out of 10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    attendance = SelectField('Attendance', choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ], default='Present')
    practical_marks = FloatField('Practical Marks', validators=[Optional(), NumberRange(min=0)])
    viva_marks = FloatField('Viva Marks', validators=[Optional(), NumberRange(min=0)])
    assignment_marks = FloatField('Assignment Marks', validators=[Optional(), NumberRange(min=0)])
    total_marks = FloatField('Total Marks', validators=[Optional(), NumberRange(min=0)])
    comments = TextAreaField('Comments', validators=[Optional()])
    lab_date = DateField('Lab Date', validators=[DataRequired()])
    submit = SubmitField('Record Performance')


class StudyMaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200), Regexp(r'^[A-Za-z0-9\s\-\'\.\,!?]+$', message='Title can only contain letters, numbers, spaces, and basic punctuation')])
    description = TextAreaField('Description', validators=[Optional()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('Upload File', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'], 'Documents only!')])
    submit = SubmitField('Upload Material')


class DetailedFeedbackForm(FlaskForm):
    faculty = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    
    # 10 Feedback Questions (1-5 rating)
    teaching_clarity = SelectField('Teaching Clarity', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    subject_knowledge = SelectField('Subject Knowledge', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    communication_skills = SelectField('Communication Skills', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    punctuality = SelectField('Punctuality', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    assignment_feedback = SelectField('Assignment Feedback Quality', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    doubt_resolution = SelectField('Doubt Resolution', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    course_completion = SelectField('Course Completion Rate', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    practical_approach = SelectField('Practical Approach', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    student_interaction = SelectField('Student Interaction', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    overall_satisfaction = SelectField('Overall Satisfaction', choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    additional_comments = TextAreaField('Additional Comments', validators=[Optional()])
    suggestions = TextAreaField('Suggestions for Improvement', validators=[Optional()])
    submit = SubmitField('Submit Feedback')


class AssignmentForm(FlaskForm):
    title = StringField('Assignment Title', validators=[DataRequired(), Length(min=5, max=200), Regexp(r'^[A-Za-z0-9\s\-\'\.\,!?]+$', message='Title can only contain letters, numbers, spaces, and basic punctuation')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    max_marks = FloatField('Maximum Marks', validators=[DataRequired(), NumberRange(min=1)])
    file = FileField('Assignment File (Optional)', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])
    submit = SubmitField('Create Assignment')


class AssignmentSubmissionForm(FlaskForm):
    submission_text = TextAreaField('Submission Text', validators=[Optional()])
    file = FileField('Upload File', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx', 'zip'], 'Documents only!')])
    submit = SubmitField('Submit Assignment')


class ModelAnswerForm(FlaskForm):
    subject_code = SelectField('Subject', choices=[
        ('OOP', 'Object Oriented Programming (OOP)'),
        ('DMs', 'Discrete Mathematics (DMs)'),
        ('DTM', 'Database Technology and Management (DTM)'),
        ('DSU', 'Data Structures (DSU)'),
        ('AMT', 'Applied Mathematics (AMT)'),
        ('SET', 'Software Engineering Technology (SET)'),
        ('DAN', 'Data Analytics (DAN)'),
        ('OSY', 'Operating Systems (OSY)')
    ], validators=[DataRequired()])
    title = StringField('Model Answer Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    semester = SelectField('Semester', choices=[
        ('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'Semester 3'), 
        ('4', 'Semester 4'), ('5', 'Semester 5'), ('6', 'Semester 6')
    ], validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired()], default='2024-25')
    file = FileField('Model Answer File', validators=[
        DataRequired(), 
        FileAllowed(['pdf', 'doc', 'docx', 'txt'], 'Documents only!')
    ])
    submit = SubmitField('Upload Model Answer')


class ExamTimetableForm(FlaskForm):
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    exam_type = SelectField('Exam Type', choices=[
        ('Unit Test 1', 'Unit Test 1'),
        ('Unit Test 2', 'Unit Test 2'),
        ('Mid Semester', 'Mid Semester'),
        ('End Semester', 'End Semester'),
        ('Practical Exam', 'Practical Exam')
    ], validators=[DataRequired()])
    exam_date = DateField('Exam Date', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=30, max=300)])
    room_number = StringField('Room Number', validators=[Optional(), Length(max=50)])
    max_marks = FloatField('Maximum Marks', validators=[DataRequired(), NumberRange(min=1)])
    instructions = TextAreaField('Instructions', validators=[Optional()])
    submit = SubmitField('Schedule Exam')


class StudentAttendanceForm(FlaskForm):
    student = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    status = SelectField('Status', choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ], default='Present')
    lecture_type = SelectField('Lecture Type', choices=[
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
        ('Tutorial', 'Tutorial')
    ], default='Theory')
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Mark Attendance')

class LeaveRequestForm(FlaskForm):
    leave_type = SelectField('Leave Type', choices=[
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('emergency', 'Emergency Leave'),
        ('personal', 'Personal Leave'),
        ('medical', 'Medical Leave')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    reason = TextAreaField('Reason', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Leave Request')

class LeaveApprovalForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('Approved', 'Approve'),
        ('Rejected', 'Reject')
    ], validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Status')

class ManageMarksForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    test_number = SelectField('Test Number', choices=[
            (1, 'Test 1'), (2, 'Test 2'), (3, 'Test 3'), 
            (4, 'Test 4'), (5, 'Test 5')
        ], coerce=int, validators=[DataRequired()])
    total_marks = FloatField('Total Marks', validators=[
        DataRequired(), 
        NumberRange(min=1, message='Total marks must be greater than 0')
    ])
    submit = SubmitField('Proceed')

class ImportMarksForm(FlaskForm):
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    test_number = SelectField('Test Number', choices=[
            (1, 'Test 1'), (2, 'Test 2'), (3, 'Test 3'), 
            (4, 'Test 4'), (5, 'Test 5')
        ], coerce=int, validators=[DataRequired()])
    total_marks = FloatField('Total Marks', validators=[
        DataRequired(), 
        NumberRange(min=1, message='Total marks must be greater than 0')
    ])
    file = FileField('Excel File', validators=[
        DataRequired(),
        FileAllowed(['xlsx', 'xls'], 'Excel files only!')
    ])
    submit = SubmitField('Import Marks')
