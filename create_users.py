from app import app, db
from models import User

with app.app_context():
    db.create_all()

    # HOD Users
    hod1 = User(username='A.B.Bhatlawande', role='hod', full_name='Dr. A.B. Bhatlawande', email='abhatlawande@sveri.edu.in')
    hod1.set_password('hod123')
    
    hod2 = User(username='R.K.Sharma', role='hod', full_name='Dr. R.K. Sharma', email='rksharma@sveri.edu.in')
    hod2.set_password('hod123')

    # Class Coordinator Users
    cc1 = User(username='M.B.Patil', role='cc', full_name='Prof. M.B. Patil', email='mbpatil@sveri.edu.in')
    cc1.set_password('staff123')
    
    cc2 = User(username='S.D.Joshi', role='cc', full_name='Prof. S.D. Joshi', email='sdjoshi@sveri.edu.in')
    cc2.set_password('staff123')
    
    cc3 = User(username='P.R.Desai', role='cc', full_name='Prof. P.R. Desai', email='prdesai@sveri.edu.in')
    cc3.set_password('staff123')

    # Faculty Users
    faculty1 = User(username='A.M.Sawant', role='faculty', full_name='Prof. A.M. Sawant', email='amsawant@sveri.edu.in')
    faculty1.set_password('staff123')
    
    faculty2 = User(username='N.V.Kulkarni', role='faculty', full_name='Prof. N.V. Kulkarni', email='nvkulkarni@sveri.edu.in')
    faculty2.set_password('staff123')
    
    faculty3 = User(username='S.S.Pawar', role='faculty', full_name='Prof. S.S. Pawar', email='sspawar@sveri.edu.in')
    faculty3.set_password('staff123')
    
    faculty4 = User(username='R.M.Jadhav', role='faculty', full_name='Prof. R.M. Jadhav', email='rmjadhav@sveri.edu.in')
    faculty4.set_password('staff123')
    
    faculty5 = User(username='V.A.More', role='faculty', full_name='Prof. V.A. More', email='vamore@sveri.edu.in')
    faculty5.set_password('staff123')

    # Student Users
    student1 = User(username='student1', role='student', full_name='Rahul Patil', email='rahul.patil@student.sveri.edu.in')
    student1.set_password('stud123')
    
    student2 = User(username='student2', role='student', full_name='Priya Sharma', email='priya.sharma@student.sveri.edu.in')
    student2.set_password('stud123')
    
    student3 = User(username='student3', role='student', full_name='Amit Kumar', email='amit.kumar@student.sveri.edu.in')
    student3.set_password('stud123')

    db.session.add_all([hod1, hod2, cc1, cc2, cc3, faculty1, faculty2, faculty3, faculty4, faculty5, student1, student2, student3])
    db.session.commit()

    print("Enhanced user database created successfully!")
    print("HOD Users: A.B.Bhatlawande, R.K.Sharma")
    print("CC Users: M.B.Patil, S.D.Joshi, P.R.Desai")
    print("Faculty Users: A.M.Sawant, N.V.Kulkarni, S.S.Pawar, R.M.Jadhav, V.A.More")
    print("Student Users: student1, student2, student3")
