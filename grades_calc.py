import sqlite3
from calc_new_curriculum import ComputationNewCurriculum
from calc_old_curriculum import ComputationOldCurriculum

def fetch_all_students():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return students

def fetch_student_grades(subject_code):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('SELECT * FROM grades WHERE subject_code = ?', (subject_code,))
    grades = c.fetchall()
    conn.close()
    return grades

def process_grades(subject_code):
    students = fetch_all_students()
    result = ""

    # Fetch grades and criteria from the databases
    students_grades = fetch_student_grades(subject_code)

    for student in students:
        student_id, last_name, first_name, middle_name, curriculum = student[:5]
        student_name = f"{first_name} {last_name}"

        # Find the student's grades
        student_grades = [grade for grade in students_grades if grade[0] == student_id]
        if student_grades:
            student_grades = student_grades[0][2:]  # Skip student_id and subject_code

            # Determine the computation class to use based on curriculum
            if curriculum == "new":
                comp = ComputationNewCurriculum()
            else:
                comp = ComputationOldCurriculum()

            # Calculate final grade
            midterm_grade = comp.calculate_midterm_finals("Midterm", student_grades)
            finals_grade = comp.calculate_midterm_finals("Finals", student_grades)
            semestral_grade = comp.calculate_semestral_grade(midterm_grade, finals_grade)

            # Assign letter grade
            numerical_equivalent = comp.get_numerical_equivalent(semestral_grade)
            remarks = comp.get_remarks(numerical_equivalent)

            result += f"{student_name} (ID: {student_id}) - Final Grade: {semestral_grade}, Letter Grade: {numerical_equivalent}, Remarks: {remarks}\n"

            # Update the grades table with the final grade (if needed)
            update_final_grade(student_id, subject_code, semestral_grade, numerical_equivalent, remarks)

    print(result)
    return result

def update_final_grade(student_id, subject_code, semestral_grade, numerical_equivalent, remarks):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute('''
        UPDATE grades
        SET semestral_grade = ?, numerical_equivalent = ?, remarks = ?
        WHERE student_id = ? AND subject_code = ?
    ''', (semestral_grade, numerical_equivalent, remarks, student_id, subject_code))
    conn.commit()
    conn.close()

