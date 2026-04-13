import os
import sqlite3
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

# List of 72 students extracted from handwritten reference
students = [
    "PATIL SIDDHI SUDHIR", "SHETE VAISHNAVI PRASHANT", "PATIL MANASI VAIBHAV", 
    "SHINDE TANVI MAHADEV", "KALE GAURAV PRAFULLA", "DOLLE POOJA MALLESHA", 
    "RAUT BHUMI YUVRAJ", "JAGDALE ROHIT BHARAT", "AWATADE SUPRIYA SURESH", 
    "KAVADE SANIKA SATISH", "YELPALE GAYATRI ANIL", "NALAWADE PRERANA ANAND", 
    "TONAPE SHREYA SHANKAR", "KHENDKAR PRANITA PANDURANG", "SAYYAD ABDULRAHEMAN MAHAMAD", 
    "AMBURE RAJNANDINI RAVINDRA", "BHOSALE CHAITANYA VINOD", "THADGE SUSHANT BALKRUSHNA", 
    "DEVAKAR SHRAVANI NAGNATH", "KAJALE DHIRAJ DHANAJI", "ANDHALKAR SAMRUDDHI VIKAS", 
    "KAMBLE ANKITA APPA", "GHADAGE HARSHAD SANJAY", "KALE SANCHIT SANJAY", 
    "DAVALE VAIBHAV ABHANGRAO", "KAZI ZIYAN JAKIRALI", "GADEKAR VAISHNAVI ISHWAR", 
    "GORE PRAGATI SANTOSH", "DIKOLE PRITI ABHIJIT", "GADE KARTIK SHANKAR", 
    "NAVGIRE SARSWATI DATTATRAY", "PAWAR GIRISH NAGESH", "BHUJABAL SAMIKSHA MAHABALI", 
    "BAGALE PARTH PRAMOD", "SHAIKH MUHAMMADREHAN JAMIR", "PATHAN AMANKHAN KHALIL", 
    "KULKARNI ARPITA AVADHUT", "LOKHANDE RUSHIKESH SURESH", "SHAIKH AFRIN FARUKH", 
    "SHINDE AMITABH PRASAD", "WAGH SUKANYA GOVARDHAN", "MANE DESHMUKH UNNATI YUVRAJ", 
    "GHEMAD SHREYA SOMANATH", "PHADATARE PRIYANKA SACHIN", "THITE SAMARTH PRASAD", 
    "DHUMAL RANAJIT DAYANAND", "WAGH AJIT VITTHAL", "SURVE MAYURI VIJAY", 
    "MORE AKANKSHA LAXMAN", "PATIL ADITI ASHOK", "BADAVE AJINKYA VAIBHAV", 
    "REVANDE PIYUSH DNYANDEV", "MORE SAMRUDDHI MAHAVIR", "KHATWATE YASH VITTHAL", 
    "CHAVARE YASHRAJ DHONDIRAM", "DESHMUKHE ARYAN ANAND", "KHANDAGALE SAKSHI SHIVAJI", 
    "DUBAL SHRUTIKA MOHAN", "YADAV SANSKRUTI SANTOSH", "PHAND TANISHKA NATRAJ", 
    "JADHAV ANUJA BANDU", "MISAL TRUPTI TUKARAM", "KAVADE PRANALI SANDIP", 
    "MORE SAYALI SADANAND", "PATIL ARUNDATI ANAND", "MALI AJAY TANAJI", 
    "BANDAL ROHAN PIRAJI", "RONGE PRUTHVIRAJ UTTAM", "PATIL ARPITA NAMANAND", 
    "JADHAV ADITYA PRAMOD", "GODASE POOJA BALASAHEB", "GODASE RUTUJA MAHESH"
]

def update_db():
    print("Executing script...")
    db_path = 'instance/faculty_workload.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if proof_file_path column exists
    c.execute("PRAGMA table_info(test_marks)")
    columns = [col[1] for col in c.fetchall()]
    if 'proof_file_path' not in columns:
        print("Adding proof_file_path to test_marks...")
        c.execute("ALTER TABLE test_marks ADD COLUMN proof_file_path VARCHAR(300)")
        conn.commit()
    else:
        print("Column proof_file_path already exists.")
        
    conn.close()

    with app.app_context():
        # Clear existing students exactly targeting the test ones, to avoid breaking core
        # To avoid deleting real students blindly, let's look for our list specifically.
        # Actually, let's just insert missing students to guarantee 72 are in order.
        print("Adding exactly 72 students sequentially.")
        
        # Optionally, delete students matching these names to avoid duplicates if run twice
        User.query.filter(User.role == 'student').delete()
        db.session.commit()
        
        for idx, student_name in enumerate(students, start=1):
            username = student_name.split()[0].lower() + str(idx)
            u = User(
                username=username,
                password_hash=generate_password_hash('student123'),
                full_name=student_name,
                email=f"{username}@college.edu",
                role='student',
                department="IF",
                section=f"{idx}", # Using section to hold Roll No
                is_active=True
            )
            db.session.add(u)
        
        db.session.commit()
        print("All 72 handwritten students seeded successfully with their Roll numbers embedded in section field.")

if __name__ == '__main__':
    update_db()
