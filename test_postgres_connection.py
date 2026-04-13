"""
PostgreSQL Connection Test Script
Departmental ERP System
"""

import psycopg2
import os
from dotenv import load_dotenv

# PostgreSQL Connection Configuration
PG_CONFIG = {
    'host': 'localhost',
    'database': 'departmental_erp',
    'user': 'postgres',
    'password': 'admin',
    'port': '5432'
}

def test_postgres_connection():
    """Test PostgreSQL connection and show database info"""
    print("🔄 Testing PostgreSQL Connection...")
    print("="*50)
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        
        print("✅ PostgreSQL Connection Successful!")
        print(f"📍 Host: {PG_CONFIG['host']}")
        print(f"🔌 Port: {PG_CONFIG['port']}")
        print(f"🗄️  Database: {PG_CONFIG['database']}")
        print(f"👤 User: {PG_CONFIG['user']}")
        
        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"🏷️  PostgreSQL Version: {version.split(',')[0]}")
        
        # Get database size
        cursor.execute("SELECT pg_size_pretty(pg_database_size(%s));", (PG_CONFIG['database'],))
        size = cursor.fetchone()[0]
        print(f"📊 Database Size: {size}")
        
        # Get table count
        cursor.execute("""
            SELECT count(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"📋 Total Tables: {table_count}")
        
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print("\n🗂️  Available Tables:")
        for i, (table_name,) in enumerate(tables, 1):
            # Get record count for each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   {i:2d}. {table_name:<25} - {count} records")
        
        # Test basic operations
        print("\n🧪 Testing Basic Operations:")
        
        # Test SELECT
        cursor.execute("SELECT 1 as test;")
        test_result = cursor.fetchone()[0]
        print(f"   ✅ SELECT Test: {test_result}")
        
        # Test INSERT/DELETE (temporary)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("INSERT INTO connection_test DEFAULT VALUES;")
        cursor.execute("SELECT COUNT(*) FROM connection_test;")
        insert_count = cursor.fetchone()[0]
        print(f"   ✅ INSERT Test: {insert_count} records")
        
        cursor.execute("DELETE FROM connection_test;")
        cursor.execute("DROP TABLE IF EXISTS connection_test;")
        print("   ✅ Cleanup Test: Temporary table dropped")
        
        # Check user permissions
        cursor.execute("SELECT current_user, current_database();")
        user_info = cursor.fetchone()
        print(f"   👤 Current User: {user_info[0]}")
        print(f"   🗄️  Current Database: {user_info[1]}")
        
        conn.close()
        
        print("\n🎉 PostgreSQL Connection Test Completed Successfully!")
        print("="*50)
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection Failed: {e}")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Check if PostgreSQL service is running")
        print("2. Verify connection parameters")
        print("3. Check firewall settings")
        print("4. Ensure database 'departmental_erp' exists")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_database_exists():
    """Check if database exists"""
    try:
        # Connect to default postgres database
        config = PG_CONFIG.copy()
        config['database'] = 'postgres'
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (PG_CONFIG['database'],))
        exists = cursor.fetchone()
        
        conn.close()
        
        return exists is not None
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 PostgreSQL Connection Test - Departmental ERP System")
    print("="*60)
    
    # Check if database exists
    print("🔍 Checking if database exists...")
    if check_database_exists():
        print(f"✅ Database '{PG_CONFIG['database']}' exists")
    else:
        print(f"❌ Database '{PG_CONFIG['database']}' does not exist")
        print("💡 Run migration script first: python migrate_to_postgresql.py")
        return
    
    # Test connection
    success = test_postgres_connection()
    
    if success:
        print("\n📝 Next Steps:")
        print("1. Open pgAdmin to view the database")
        print("2. Run the Flask application: python app.py")
        print("3. Test the web interface")
    else:
        print("\n🔧 Please fix connection issues before proceeding")

if __name__ == "__main__":
    main()
