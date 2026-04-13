from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import sys

def create_principal_user():
    with app.app_context():
        # Check if principal user already exists
        existing_principal = User.query.filter_by(username='N.D.Misal').first()
        if existing_principal:
            print("Principal user 'N.D.Misal' already exists!")
            print(f"Current role: {existing_principal.role}")
            print(f"Current email: {existing_principal.email}")
            print("Updating password to 'principal123'...")
            existing_principal.set_password('principal123')
            existing_principal.role = 'principal'
            existing_principal.is_active = True
            db.session.commit()
            print("Password updated successfully!")
        else:
            # Create new principal user
            principal_user = User(
                username='N.D.Misal',
                email='principal@college.edu',
                full_name='Dr. N.D. Misal',
                role='principal',
                is_active=True
            )
            principal_user.set_password('principal123')
            
            try:
                db.session.add(principal_user)
                db.session.commit()
                print("Principal user created successfully!")
                print("Username: N.D.Misal")
                print("Password: principal123")
                print("Role: principal")
            except Exception as e:
                print(f"Error creating principal user: {e}")
                db.session.rollback()

if __name__ == '__main__':
    create_principal_user()
