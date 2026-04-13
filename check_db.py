import sqlite3
c = sqlite3.connect('faculty_workload.db').cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
