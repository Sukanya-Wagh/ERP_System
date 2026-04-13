"""
Departmental ERP System - SQLite to PostgreSQL Migration Script
Author: Migration Assistant
Date: 2026-04-13
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import json
from sqlalchemy import create_engine
from extension import db
from models import *
from app import app

# PostgreSQL Connection Configuration
PG_CONFIG = {
    'host': 'localhost',
    'database': 'departmental_erp',
    'user': 'postgres',
    'password': 'admin',  # Change this to your PostgreSQL password
    'port': '5432'
}

# SQLite Database Path
SQLITE_DB = 'faculty_workload.db'

class DatabaseMigrator:
    def __init__(self):
        self.pg_conn = None
        self.sqlite_conn = None
        
    def connect_postgresql(self):
        """Connect to PostgreSQL database"""
        try:
            self.pg_conn = psycopg2.connect(**PG_CONFIG)
            self.pg_conn.autocommit = True
            print("✅ PostgreSQL connection successful")
            return True
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            return False
    
    def connect_sqlite(self):
        """Connect to SQLite database"""
        try:
            self.sqlite_conn = sqlite3.connect(SQLITE_DB)
            self.sqlite_conn.row_factory = sqlite3.Row
            print("✅ SQLite connection successful")
            return True
        except Exception as e:
            print(f"❌ SQLite connection failed: {e}")
            return False
    
    def create_postgresql_database(self):
        """Create PostgreSQL database if it doesn't exist"""
        print("🔄 Creating PostgreSQL database...")
        
        # Connect to PostgreSQL default database
        conn_config = PG_CONFIG.copy()
        conn_config['database'] = 'postgres'
        
        try:
            conn = psycopg2.connect(**conn_config)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Drop database if exists and create new one
            cursor.execute(f"DROP DATABASE IF EXISTS {PG_CONFIG['database']}")
            cursor.execute(f"CREATE DATABASE {PG_CONFIG['database']}")
            
            conn.close()
            print(f"✅ Database '{PG_CONFIG['database']}' created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            return False
    
    def create_postgresql_schema(self):
        """Create all tables in PostgreSQL"""
        print("🔄 Creating PostgreSQL schema...")
        
        with self.pg_conn.cursor() as cursor:
            # Create User table
            cursor.execute("""
                CREATE TABLE user (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    password_hash VARCHAR(256),
                    role VARCHAR(20) NOT NULL,
                    email VARCHAR(120) UNIQUE,
                    phone VARCHAR(15),
                    full_name VARCHAR(200),
                    department VARCHAR(100),
                    profile_picture VARCHAR(200),
                    date_joined TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    roll_number VARCHAR(20),
                    section VARCHAR(10)
                );
            """)
            
            # Create Subject table
            cursor.execute("""
                CREATE TABLE subject (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    code VARCHAR(20) UNIQUE NOT NULL,
                    department VARCHAR(100),
                    semester VARCHAR(20),
                    credits INTEGER DEFAULT 3,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create other essential tables
            cursor.execute("""
                CREATE TABLE complaint (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    priority VARCHAR(20) NOT NULL,
                    submitted_by INTEGER REFERENCES user(id),
                    status VARCHAR(20) DEFAULT 'Pending',
                    comments TEXT,
                    resolved_by INTEGER REFERENCES user(id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP
                );
            """)
            
            cursor.execute("""
                CREATE TABLE workload (
                    id SERIAL PRIMARY KEY,
                    faculty_id INTEGER REFERENCES user(id),
                    subject VARCHAR(150),
                    subject_id INTEGER REFERENCES subject(id),
                    workload_type VARCHAR(50) DEFAULT 'Theory',
                    semester VARCHAR(20) DEFAULT 'Current',
                    hours INTEGER NOT NULL,
                    assigned_by INTEGER REFERENCES user(id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("""
                CREATE TABLE marks (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER REFERENCES user(id),
                    cc_id INTEGER REFERENCES user(id),
                    subject VARCHAR(100) NOT NULL,
                    marks_obtained FLOAT NOT NULL,
                    total_marks FLOAT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("""
                CREATE TABLE notification (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user(id),
                    title VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("""
                CREATE TABLE attendance (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user(id),
                    date DATE NOT NULL,
                    check_in TIMESTAMP,
                    check_out TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'Present',
                    hours_worked FLOAT DEFAULT 0.0,
                    notes TEXT
                );
            """)
            
        print("✅ PostgreSQL schema created successfully")
    
    def migrate_data_from_sqlalchemy(self):
        """Migrate data using SQLAlchemy models"""
        print("🔄 Starting data migration using SQLAlchemy...")
        
        with app.app_context():
            # Get all models
            tables = [
                ('user', User),
                ('subject', Subject),
                ('complaint', Complaint),
                ('workload', Workload),
                ('marks', Marks),
                ('notification', Notification),
                ('attendance', Attendance)
            ]
            
            total_migrated = 0
            
            for table_name, model in tables:
                print(f"📋 Migrating table: {table_name}")
                
                # Get data from SQLite
                data = model.query.all()
                
                if not data:
                    print(f"   📭 No data in {table_name}")
                    continue
                
                # Convert to list of dictionaries
                records = []
                for record in data:
                    record_dict = {}
                    for column in record.__table__.columns:
                        value = getattr(record, column.name)
                        # Handle datetime objects
                        if hasattr(value, 'isoformat'):
                            record_dict[column.name] = value.isoformat()
                        else:
                            record_dict[column.name] = value
                    records.append(record_dict)
                
                # Insert into PostgreSQL using raw SQL
                if records:
                    with self.pg_conn.cursor() as pg_cursor:
                        for record in records:
                            columns = list(record.keys())
                            placeholders = ', '.join(['%s'] * len(columns))
                            columns_str = ', '.join(columns)
                            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                            
                            values = [record[col] for col in columns]
                            
                            try:
                                pg_cursor.execute(query, values)
                                total_migrated += 1
                            except Exception as e:
                                print(f"   ⚠️  Error inserting record: {e}")
                
                print(f"   ✅ Migrated {len(records)} records from {table_name}")
            
            print(f"✅ Data migration completed. Total records migrated: {total_migrated}")
    
    def update_app_config(self):
        """Update app configuration to use PostgreSQL"""
        print("🔄 Updating application configuration...")
        
        # Read current config.py
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Update database URI
        new_content = content.replace(
            "SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///faculty_workload.db'",
            f"SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}'"
        )
        
        # Write updated config
        with open('config.py', 'w') as f:
            f.write(new_content)
        
        # Also update app.py
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        new_app_content = app_content.replace(
            "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faculty_workload.db'",
            f"app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}'"
        )
        
        with open('app.py', 'w') as f:
            f.write(new_app_content)
        
        print("✅ Configuration updated successfully")
    
    def run_migration(self):
        """Run complete migration process"""
        print("🚀 Starting SQLite to PostgreSQL Migration")
        print("="*60)
        
        # Create database first
        if not self.create_postgresql_database():
            return False
        
        # Connect to databases
        if not self.connect_postgresql():
            return False
        
        if not self.connect_sqlite():
            return False
        
        try:
            # Create schema
            self.create_postgresql_schema()
            
            # Migrate data
            self.migrate_data_from_sqlalchemy()
            
            # Update configuration
            self.update_app_config()
            
            print("\n🎉 Migration completed successfully!")
            print("="*60)
            print("📝 Next Steps:")
            print("1. Install PostgreSQL driver: pip install psycopg2-binary")
            print("2. Test the application: python app.py")
            print("3. Open pgAdmin to view the database")
            print("4. Database name:", PG_CONFIG['database'])
            
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
        
        finally:
            if self.pg_conn:
                self.pg_conn.close()
            if self.sqlite_conn:
                self.sqlite_conn.close()

def setup_postgresql_connection():
    """Setup PostgreSQL connection string"""
    # Update these with your PostgreSQL credentials
    pg_user = 'postgres'  # Your PostgreSQL username
    pg_password = 'your_password'  # Your PostgreSQL password
    pg_host = 'localhost'
    pg_port = '5432'
    pg_database = 'departmental_erp'
    
    return f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'

def main():
    migrator = DatabaseMigrator()
    success = migrator.run_migration()
    
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")

if __name__ == "__main__":
    main()
