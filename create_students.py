from app import app, db
from models import User

students_list = [
    "PATIL MANASI VAIBHAV",
    "SHINDE TANVI MAHADEV",
    "KALE GAURAV PRAFULLA",
    "DOLLE POOJA MALLESHA",
    "RAUT BHUMI YUVRAJ",
    "JAGDALE ROHIT BHARAT",
    "AWATADE SUPRIYA SURESH",
    "KAVADE SANIKA SATISH",
    "YELPALE GAYATRI ANIL",
    "NALAWADE PRERANA ANAND",
    "TONAPE SHREYA SHANKAR",
    "KHENDKAR PRANITA PANDURANG",
    "SAYYAD ABDULRAHEMAN MAHAMAD",
    "AMBURE RAJNANDINI RAVINDRA",
    "BHOSALE CIIATTANYA VINOD",
    "THADGE SUSHANT BALKRUSHNA",
    "DEVAKAR SIRAVANI NAGNATH",
    "KAJALE DHIRAJ DHANAJI",
    "ANDHALKAR SAMRUDDHI VIKAS",
    "KAMBLE ANKITA APPA",
    "GHADAGE HARSHAD SANJAY",
    "KALE SANCHIT SANJAY",
    "DAVALE VAIBHAV ABHANGRAO",
    "KAZI ZIYAN JAKIRALI",
    "GADEKAR VAISHNAVI ISHWAR",
    "GORE PRAGATI SANTOSH",
    "DIKOLE PRITI ABHIJIT",
    "GADE KARTIK SHANKAR",
    "NAVGIRE SARSWATI DATTATRAY",
    "PAWAR GIRISH NAGESH",
    "BHUJABAL SANIKSHA MAHABALI",
    "BAGALE PARTH PRAMOD",
    "SHAIKH MUHAMMADREHAN JAMIR",
    "PATHAN AMANKHAN KHALIL",
    "KULKARNI ARPITA AVADHUT",
    "LOKHANDE RUSHIKESH SURESH",
    "ATHAWALE SAMIKSHA SACHIN",
    "SHAIKH AFRIN FARUKH",
    "SHINDE AMITABH PRASAD",
    "WAGH SUKANYA GOVARDHAN",
    "MANE DESHMUKH UNNATI YUVRAJ",
    "GHEMAD SHREYA SOMANATH",
    "PHADATARE PRIYANKA SACHIN",
    "THITE SAMARTH PRASAD",
    "NIKAM HRISHIKESH HANMANT",
    "DHUMAL RANAJIT DAYANAND",
    "BODAKE ARYAN NETAJI",
    "WAGH AJIT VITTHAL",
    "SURVE MAYURI VIJAY",
    "MORE AKANKSHA LAXMAN",
    "PATIL ADITI ASHOK",
    "BADAVE AJINKYA VAIBHAV",
    "REVANDE PIVUSH DNYANDEV",
    "MORE SAMRUDDIH MAHAVIR",
    "KHATWATE YASH VITTHAL",
    "CHAVARE YASHRAJ DHONDIRAM",
    "DESHMUKHE ARYAN ANAND",
    "KHANDAGALE SAKSHI SHIVAJI",
    "DUBAL SHRUTIKA MOHAN",
    "YADAV SANSKRUTI SANTOSH",
    "PHAND TANISIIKA NATRAJ",
    "JADHAV ANUJA BANDU",
    "MISAL TRUPTI TUKARAM",
    "KAVADE PRANALI SANDIP",
    "MORE SAYALI SADANAND",
    "PATIL ARUNDATI ANAND",
    "SHETE VAISHNAVI PRASHANT",
    "PATIL SIDDIH SUDHIR",
    "MALI AJAY TANAJI",
    "GODASE POOJA BALASAHEB",
    "GODASE RUTUJA MAHESH"
]

with app.app_context():
    print("Creating student users...")
    
    for i, student_name in enumerate(students_list, 1):
        # Create username from first name and roll number
        first_name = student_name.split()[0].lower()
        username = f"{first_name}{i:02d}"
        password = f"student{i:02d}"
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            student = User(username=username, role='student')
            student.set_password(password)
            db.session.add(student)
            print(f"Created: {username} - {student_name}")
        else:
            print(f"Already exists: {username}")
    
    db.session.commit()
    print(f"\nTotal {len(students_list)} students processed!")
    print("\nSample login credentials:")
    print("Username: patil01, Password: student01")
    print("Username: shinde02, Password: student02")
    print("Username: kale03, Password: student03")
