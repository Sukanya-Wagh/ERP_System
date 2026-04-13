import sqlite3
import os

db_path = 'faculty_workload.db'
if os.path.exists(db_path):
    print(f'Database file exists: {os.path.getsize(db_path)} bytes')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables in database: {[t[0] for t in tables]}")
    
    for table_info in tables:
        table_name = table_info[0]
        print(f"\nTable: {table_name}")
        
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"  Columns: {[col[1] for col in columns]}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  Row count: {count}")
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            rows = cursor.fetchall()
            print(f"  Sample data (first 2 rows):")
            for row in rows:
                print(f"    {row}")
    
    conn.close()
else:
    print(f"Database file does not exist at: {db_path}")