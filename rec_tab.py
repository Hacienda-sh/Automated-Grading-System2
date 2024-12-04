import sqlite3


def setup_record_db():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()

    # Create Grades Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            student_id TEXT,
            subject_code TEXT,
            quiz INTEGER DEFAULT 0,
            midterm_exam INTEGER DEFAULT 0,
            finals_exam INTEGER DEFAULT 0,
            performance_based_act INTEGER DEFAULT 0,
            PRIMARY KEY (student_id, subject_code),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(subject_code) REFERENCES subjects(subject_code)
        )
    ''')

    conn.commit()
    conn.close()

def add_score(student_id, subject_code, quiz, midterm_exam, finals_exam, performance_based_act):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO grades (student_id, subject_code, quiz, midterm_exam, finals_exam, performance_based_act)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, subject_code, quiz, midterm_exam, finals_exam, performance_based_act))
    conn.commit()
    conn.close()

def fetch_student_grades(subject_code):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute("SELECT * FROM grades WHERE subject_code = ?", (subject_code,))
    grades = c.fetchall()
    conn.close()
    return grades


def update_grade(student_id, subject_code, column_name, new_value):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute(f"UPDATE grades SET {column_name} = ? WHERE student_id = ? AND subject_code = ?",
              (new_value, student_id, subject_code))
    conn.commit()
    conn.close()

# Delete student grades from the grades database by student ID
def delete_student_grades(student_id):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    if c.rowcount > 0:
        conn.commit()
    conn.close()

# Ensure the tables are set up
setup_record_db()