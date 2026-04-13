from app import app
from models import *
from extension import db

def create_database_tables_only():
    with app.app_context():
        print("🔄 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Show table info
        import sqlite3
        conn = sqlite3.connect('faculty_workload.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table[0]}")
        
        conn.close()

if __name__ == "__main__":
    create_database_tables_only()
