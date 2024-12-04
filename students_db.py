import sqlite3
from rec_tab import delete_student_grades, setup_record_db

def setup_students_info_db():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()

    # Create Students Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            last_name TEXT,
            first_name TEXT,
            middle_name TEXT,
            curriculum TEXT,
            batch TEXT,
            course TEXT,
            sex TEXT,
            date_of_birth TEXT,
            place_of_birth TEXT,
            postal_address TEXT,
            home_pnumber TEXT,
            mobile_pnumber TEXT,
            email TEXT,
            residential_address TEXT,
            guardian_name TEXT,
            guardian_contact TEXT
        )
    ''')


    # Create Performance-Based Activities Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS performance_based_activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT,
            activity_name TEXT,
            activity_weight REAL,
            FOREIGN KEY(subject_code) REFERENCES subjects(subject_code)
        )
    ''')

    conn.commit()
    conn.close()


def add_student(student_id, last_name, first_name, middle_name, curriculum, batch, course, sex, date_of_birth,
                place_of_birth, postal_address, home_pnumber, mobile_pnumber, email, residential_address, guardian_name,
                guardian_contact):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO students (student_id, last_name, first_name, middle_name, curriculum, batch, course, sex, date_of_birth, place_of_birth, postal_address, home_pnumber, mobile_pnumber, email, residential_address, guardian_name, guardian_contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, last_name, first_name, middle_name, curriculum, batch, course, sex, date_of_birth, place_of_birth,
          postal_address, home_pnumber, mobile_pnumber, email, residential_address, guardian_name, guardian_contact))
    conn.commit()
    conn.close()

# Fetch a student by their ID
def fetch_student_by_id(student_id):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM students WHERE student_id = ? ''', (student_id,))
    student = c.fetchone()
    conn.close()
    return student

# Check if a student ID already exists
def student_exists(student_id):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM students WHERE id = ?", (student_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def delete_student(student_id):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    # First, delete the student's grades from the grades database
    delete_student_grades(student_id)
    # Now, delete the student from the students_info.db
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if c.rowcount > 0:  # Check if any rows were affected (student existed)
        conn.commit()
        conn.close()
        return True  # Deletion successful
    conn.close()
    return False  # Student ID not found

def add_performance_based_activity(subject_code, activity_name, activity_weight):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO performance_based_activities (subject_code, activity_name, activity_weight)
        VALUES (?, ?, ?)
    ''', (subject_code, activity_name, activity_weight))
    conn.commit()
    conn.close()

# Fetch all students (summary view)
def fetch_all_students():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return students

# def fetch_all_students():
#     conn = sqlite3.connect('students_info.db')
#     c = conn.cursor()
#     c.execute('''
#         SELECT student_id, last_name, first_name, middle_name, curriculum, course
#         FROM students
#     ''')
#     students = c.fetchall()
#     conn.close()
#     return students



# Update student information
def update_student(student_id, last_name = None, first_name = None, middle_name = None, curriculum = None, batch = None, course = None, sex = None, date_of_birth = None,
                place_of_birth = None, postal_address = None, home_pnumber = None, mobile_pnumber = None, email = None, residential_address = None, guardian_name= None,
                guardian_contact = None):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    updates = []
    values = []

    # Add fields to update dynamically
    if last_name:
        updates.append("name = ?")
        values.append(last_name)
    if first_name:
        updates.append("name = ?")
        values.append(first_name)
    if middle_name:
        updates.append("name = ?")
        values.append(middle_name)
    if curriculum:
        updates.append("curriculum = ?")
        values.append(curriculum)
    if batch:
        updates.append("batch = ?")
        values.append(batch)
    if course:
        updates.append("course = ?")
        values.append(course)
    if sex:
        updates.append("course = ?")
        values.append(sex)
    if date_of_birth:
        updates.append("date_of_birth = ?")
        values.append(date_of_birth)
    if place_of_birth:
        updates.append("place_of_birth = ?")
        values.append(place_of_birth)
    if postal_address:
        updates.append("postal address = ?")
        values.append(postal_address)
    if home_pnumber:
        updates.append("home phone number = ?")
        values.append(home_pnumber)
    if mobile_pnumber:
        updates.append("mobile phone number = ?")
        values.append(mobile_pnumber)
    if email:
        updates.append("email = ?")
        values.append(email)
    if residential_address:
        updates.append("residential address = ?")
        values.append(residential_address)
    if guardian_name:
        updates.append("guardian_name = ?")
        values.append(guardian_name)
    if guardian_contact:
        updates.append("guardian_contact = ?")
        values.append(guardian_contact)

    if updates:  # Proceed only if there are updates
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
        values.append(student_id)
        c.execute(query, tuple(values))
        conn.commit()
    conn.close()

def update_student_table():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    columns_to_add = [
        ("curriculum", "TEXT"),
        ("batch", "TEXT"),
        ("course", "TEXT"),
        ("sex", "TEXT"),
        ("date_of_birth", "TEXT"),
        ("place_of_birth", "TEXT"),
        ("postal_address", "TEXT"),
        ("home_pnumber", "TEXT"),
        ("mobile_pnumber", "TEXT"),
        ("email", "TEXT"),
        ("residential_address", "TEXT"),
        ("guardian_name", "TEXT"),
        ("guardian_contact", "TEXT")
    ]
    for column, column_type in columns_to_add:
        try:
            c.execute(f"ALTER TABLE students ADD COLUMN {column} {column_type};")
        except sqlite3.OperationalError:
            pass  # Ignore error if column already exists
    conn.commit()
    conn.close()



# Ensure the tables are set up
setup_students_info_db()
