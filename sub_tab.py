import sqlite3
from tkinter import messagebox

def setup_sub_db():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    # Create the `subjects` table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            sub_code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    ''')
    # Create the `grading_criteria` table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS grading_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            exams_weight REAL NOT NULL,
            projects_weight REAL NOT NULL,
            quizzes_weight REAL NOT NULL,
            FOREIGN KEY(subject_name) REFERENCES subjects(name)
        )
    ''')
    conn.commit()
    conn.close()

# Add subject
def add_subject(subject_name, sub_code, semester):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    try:
        # Check if subject already exists
        c.execute("SELECT sub_code FROM subjects WHERE sub_code = ?", (sub_code,))
        if c.fetchone():
            messagebox.showerror("Error", "Subject with this subject code already exists.")
        else:
            c.execute("INSERT INTO subjects (name, sub_code, semester) VALUES (?, ?, ?)", (subject_name, sub_code, semester))
            conn.commit()
            messagebox.showinfo("Success", "Subject added successfully.")
    finally:
        conn.close()

# Fetch all subjects
def fetch_all_subjects():
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute("SELECT name, sub_code, semester FROM subjects")
    subjects = c.fetchall()
    conn.close()
    return subjects

# Delete a subject
def delete_subject(sub_code):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM subjects WHERE sub_code = ?", (sub_code,))
        if c.rowcount == 0:  # No rows were deleted, meaning subject did not exist
            messagebox.showwarning("Error", "Subject not found.")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Subject deleted successfully.")
    finally:
        conn.close()

# Save the edited grading criteria
def save_grading_criteria(subject_name, exams_weight, projects_weight, quizzes_weight):
    conn = sqlite3.connect('students_info.db')
    c = conn.cursor()
    c.execute(''' 
        INSERT OR REPLACE INTO grading_criteria (subject_name, exams_weight, projects_weight, quizzes_weight) 
        VALUES (?, ?, ?, ?) 
    ''', (subject_name, exams_weight, projects_weight, quizzes_weight))
    conn.commit()
    conn.close()

# Run the database setup to ensure tables are created
setup_sub_db()
