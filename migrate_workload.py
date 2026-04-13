import sqlite3

conn = sqlite3.connect('instance/faculty_workload.db')
cursor = conn.cursor()

# Show current columns
cursor.execute('PRAGMA table_info(workload)')
cols = cursor.fetchall()
print('Current workload columns:')
for c in cols:
    print(c)

existing_cols = [c[1] for c in cols]

# Add subject_id if missing
if 'subject_id' not in existing_cols:
    cursor.execute('ALTER TABLE workload ADD COLUMN subject_id INTEGER REFERENCES subject(id)')
    print('Added subject_id column')
else:
    print('subject_id already exists')

# Add workload_type if missing
if 'workload_type' not in existing_cols:
    cursor.execute("ALTER TABLE workload ADD COLUMN workload_type VARCHAR(50) DEFAULT 'Theory'")
    print('Added workload_type column')
else:
    print('workload_type already exists')

# Add semester if missing
if 'semester' not in existing_cols:
    cursor.execute("ALTER TABLE workload ADD COLUMN semester VARCHAR(20) DEFAULT 'Current'")
    print('Added semester column')
else:
    print('semester already exists')

conn.commit()

# Verify final columns
cursor.execute('PRAGMA table_info(workload)')
cols = cursor.fetchall()
print('\nUpdated workload columns:')
for c in cols:
    print(c)

conn.close()
print('\nMigration complete!')
