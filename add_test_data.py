from app import app, db
from models import Subject, User, FacultySubject

def add_test_data():
    with app.app_context():
        print("Adding test subjects...")
        
        # Add test subjects
        subjects = [
            Subject(name='Mathematics', code='MATH101'),
            Subject(name='Physics', code='PHY101'),
            Subject(name='Chemistry', code='CHEM101'),
            Subject(name='Computer Science', code='CS101'),
            Subject(name='Electronics', code='EC101')
        ]
        
        for subject in subjects:
            if not Subject.query.filter_by(code=subject.code).first():
                db.session.add(subject)
        
        db.session.commit()
        print(f"Added {len(subjects)} subjects")
        
        # Get first faculty member
        faculty = User.query.filter_by(role='faculty').first()
        if not faculty:
            print("No faculty found. Please create a faculty user first.")
            return
            
        print(f"Assigning subjects to faculty: {faculty.username}")
        
        # Assign all subjects to faculty
        for subject in Subject.query.all():
            if not FacultySubject.query.filter_by(
                faculty_id=faculty.id, 
                subject_id=subject.id
            ).first():
                fs = FacultySubject(faculty_id=faculty.id, subject_id=subject.id)
                db.session.add(fs)
        
        db.session.commit()
        print("Subjects assigned successfully!")

if __name__ == '__main__':
    add_test_data()
