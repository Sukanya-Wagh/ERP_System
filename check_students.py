import sqlite3
conn = sqlite3.connect('instance/faculty_workload.db')
cursor = conn.cursor()
cursor.execute("SELECT username, full_name, role, password_hash FROM user WHERE role='student' LIMIT 20")
rows = cursor.fetchall()
for r in rows:
    has_pwd = 'YES' if r[3] else 'NO'
    print(f"username={r[0]}, name={r[1]}, has_password={has_pwd}")
conn.close()
