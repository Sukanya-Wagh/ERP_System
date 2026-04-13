from app import app, db
from models import LeaveRequest

def migrate_database():
    """Add LeaveRequest table to existing database"""
    with app.app_context():
        # Create the LeaveRequest table
        db.create_all()
        print("Database migration completed successfully!")
        print("LeaveRequest table has been created.")

if __name__ == '__main__':
    migrate_database()
