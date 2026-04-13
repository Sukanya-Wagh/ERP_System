import sqlite3
from models import *

def get_database_info():
    conn = sqlite3.connect('faculty_workload.db')
    cursor = conn.cursor()
    
    print("=== FACULTY WORKLOAD MANAGEMENT SYSTEM DATABASE ===\n")
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if not tables:
        print("📭 No tables found in database!")
        print("Database appears to be empty.")
        return
    
    print(f"📊 Total Tables: {len(tables)}\n")
    
    for table in tables:
        table_name = table[0]
        print(f"🗂️  TABLE: {table_name.upper()}")
        print("-" * 50)
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print("📋 Columns:")
        for col in columns:
            nullable = "NULL" if col[3] == 0 else "NOT NULL"
            default = f" DEFAULT {col[4]}" if col[4] is not None else ""
            print(f"   • {col[1]} ({col[2]}) {nullable}{default}")
        
        # Get record count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"📈 Total Records: {count}")
        
        # Show sample data if records exist
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            sample_data = cursor.fetchall()
            print("📄 Sample Data:")
            for i, row in enumerate(sample_data, 1):
                print(f"   Row {i}: {row}")
        
        print("\n" + "="*60 + "\n")
    
    conn.close()

if __name__ == "__main__":
    get_database_info()
