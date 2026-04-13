#!/usr/bin/env python3
"""
Migration script to update Complaint and LeaveRequest models
Run this script to migrate your existing database to the new schema
"""

from app import app, db
from models import User, Complaint, LeaveRequest
from sqlalchemy import text
import sys

def migrate_database():
    """Migrate the database to new schema"""
    with app.app_context():
        try:
            print("Starting database migration...")
            
            # Check if we need to migrate complaints table
            try:
                # Try to query old structure
                result = db.session.execute(text("SELECT student_id, content FROM complaint LIMIT 1"))
                old_complaints_exist = True
                print("Found old complaint structure, migrating...")
            except Exception:
                old_complaints_exist = False
                print("Complaint table already migrated or doesn't exist")
            
            # Check if we need to migrate leave_request table
            try:
                # Try to query old structure
                result = db.session.execute(text("SELECT user_id FROM leave_request LIMIT 1"))
                old_leave_requests_exist = True
                print("Found old leave request structure, migrating...")
            except Exception:
                old_leave_requests_exist = False
                print("Leave request table already migrated or doesn't exist")
            
            if old_complaints_exist:
                # Backup old complaint data
                print("Backing up old complaint data...")
                old_complaints = db.session.execute(text("""
                    SELECT id, student_id, content, status, timestamp 
                    FROM complaint
                """)).fetchall()
                
                # Drop old table and create new one
                print("Recreating complaint table...")
                db.session.execute(text("DROP TABLE IF EXISTS complaint"))
                db.session.commit()
                
                # Create new table structure
                db.create_all()
                
                # Migrate old data to new structure
                print(f"Migrating {len(old_complaints)} complaint records...")
                for old_complaint in old_complaints:
                    new_complaint = Complaint(
                        title="Migrated Complaint",
                        description=old_complaint[2],  # content -> description
                        category="other",
                        priority="medium",
                        submitted_by=old_complaint[1],  # student_id -> submitted_by
                        status=old_complaint[3],
                        timestamp=old_complaint[4]
                    )
                    db.session.add(new_complaint)
                
                db.session.commit()
                print("Complaint migration completed!")
            
            if old_leave_requests_exist:
                # Backup old leave request data
                print("Backing up old leave request data...")
                old_requests = db.session.execute(text("""
                    SELECT id, user_id, approver_id, leave_type, start_date, end_date, 
                           reason, status, comments, timestamp 
                    FROM leave_request
                """)).fetchall()
                
                # Drop old table and create new one
                print("Recreating leave_request table...")
                db.session.execute(text("DROP TABLE IF EXISTS leave_request"))
                db.session.commit()
                
                # Create new table structure
                db.create_all()
                
                # Migrate old data to new structure
                print(f"Migrating {len(old_requests)} leave request records...")
                for old_request in old_requests:
                    new_request = LeaveRequest(
                        requester_id=old_request[1],  # user_id -> requester_id
                        approver_id=old_request[2],
                        leave_type=old_request[3],
                        start_date=old_request[4],
                        end_date=old_request[5],
                        reason=old_request[6],
                        status=old_request[7],
                        comments=old_request[8],
                        timestamp=old_request[9]
                    )
                    db.session.add(new_request)
                
                db.session.commit()
                print("Leave request migration completed!")
            
            # Ensure all tables are created
            db.create_all()
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Migration failed: {str(e)}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()