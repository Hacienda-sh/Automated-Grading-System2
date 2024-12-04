import sqlite3

def fetch_subjects():
    return execute_query("SELECT sub_code, name FROM subjects")

def fetch_student_names(subject_code):
    query = """
        SELECT s.student_id, s.first_name || ' ' || s.last_name
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.subject_code = ?
    """
    return execute_query(query, (subject_code,))

def fetch_enrolled_subjects(student_id):
    query = """
        SELECT e.subject_code, s.name
        FROM enrollments e
        JOIN subjects s ON e.subject_code = s.sub_code
        WHERE e.student_id = ?
    """
    return execute_query(query, (student_id,))

def fetch_enrolled_students(subject_code):
    query = """
        SELECT s.student_id, s.first_name || ' ' || s.last_name
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.subject_code = ?
    """
    return execute_query(query, (subject_code,))

def update_grade(student_id, subject_code, column_name, new_value, period):
    query = f"""
        UPDATE grades
        SET {column_name} = ?
        WHERE student_id = ? AND subject_code = ? AND period = ?
    """
    execute_query(query, (new_value, student_id, subject_code, period), commit=True)

def execute_query(query, params=(), commit=False):
    conn = sqlite3.connect('students_info.db')
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return results

