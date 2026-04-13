from app import app, db
from models import User

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created")
    
    # Check if users exist
    users_to_create = [
        {
            'username': 'N.D.Misal',
            'password': 'principal123',
            'full_name': 'Dr. N.D. Misal',
            'email': 'principal@college.edu',
            'role': 'principal'
        },
        {
            'username': 'patil65',
            'password': 'student65',
            'full_name': 'PATIL ARUNDATI ANAND',
            'email': 'patil65@college.edu',
            'role': 'student',
            'roll_number': '65'
        },
        {
            'username': 'A.S.Bhatlavande',
            'password': 'hod123',
            'full_name': 'A.S. Bhatlavande',
            'email': 'hod@college.edu',
            'role': 'hod'
        }
    ]
    
    for user_data in users_to_create:
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                full_name=user_data['full_name'],
                email=user_data['email'],
                role=user_data['role'],
                is_active=True
            )
            if 'roll_number' in user_data:
                user.roll_number = user_data['roll_number']
            
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"Created user: {user_data['username']}")
        else:
            print(f"User {user_data['username']} already exists")
    
    db.session.commit()
    print("Users added successfully!")