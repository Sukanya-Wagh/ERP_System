#!/usr/bin/env python3
"""
Database Migration Script
Adds new columns to existing database tables
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate existing database to new schema"""
    db_path = 'instance/faculty_workload.db'
    
    if not os.path.exists(db_path):
        print("Database not found. Creating new database with updated schema.")
        return
    
    print("Starting database migration...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add new columns to user table if they don't exist
        new_columns = [
            ('email', 'VARCHAR(120)'),
            ('phone', 'VARCHAR(15)'),
            ('full_name', 'VARCHAR(200)'),
            ('department', 'VARCHAR(100)'),
            ('profile_picture', 'VARCHAR(200)'),
            ('date_joined', 'DATETIME'),
            ('last_login', 'DATETIME'),
            ('is_active', 'BOOLEAN')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                try:
                    if column_name == 'date_joined':
                        cursor.execute(f"ALTER TABLE user ADD COLUMN {column_name} {column_type} DEFAULT '{datetime.utcnow().isoformat()}'")
                    elif column_name == 'is_active':
                        cursor.execute(f"ALTER TABLE user ADD COLUMN {column_name} {column_type} DEFAULT 1")
                    else:
                        cursor.execute(f"ALTER TABLE user ADD COLUMN {column_name} {column_type}")
                    print(f"Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"Column {column_name} might already exist: {e}")
        
        # Create new tables if they don't exist
        new_tables = [
            """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                check_in DATETIME,
                check_out DATETIME,
                status VARCHAR(20) DEFAULT 'Present',
                hours_worked FLOAT DEFAULT 0.0,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty_id INTEGER NOT NULL,
                subject VARCHAR(150) NOT NULL,
                day_of_week VARCHAR(10) NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                room_number VARCHAR(50),
                semester VARCHAR(20),
                academic_year VARCHAR(20),
                FOREIGN KEY (faculty_id) REFERENCES user (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                report_type VARCHAR(50) NOT NULL,
                generated_by INTEGER NOT NULL,
                file_path VARCHAR(300),
                parameters TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (generated_by) REFERENCES user (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_by INTEGER,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (updated_by) REFERENCES user (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action VARCHAR(100) NOT NULL,
                table_name VARCHAR(50),
                record_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
            """
        ]
        
        for table_sql in new_tables:
            cursor.execute(table_sql)
            print(f"Created/verified table")
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
