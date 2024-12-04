import sqlite3
from tkinter import messagebox, ttk
import tkinter as tk
from data_operations import fetch_subjects

def create_enrollments_table():
    query = """
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_code TEXT NOT NULL,
            period TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_code) REFERENCES subjects(sub_code)
        );
    """
    execute_query(query, commit=True)

def enroll_student_in_subject(student_id, subject_code):
    execute_query("INSERT INTO enrollments (student_id, subject_code) VALUES (?, ?)", (student_id, subject_code), commit=True)
    messagebox.showinfo("Success", "Student enrolled in subject successfully.")

def fetch_enrolled_students(subject_code):
    query = """
        SELECT s.student_id, s.first_name || ' ' || s.last_name
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.subject_code = ?
    """
    return execute_query(query, (subject_code,))

def enroll_student_in_subject_window(students_tree):
    selected_item = students_tree.focus()
    student_id = students_tree.item(selected_item, "values")[0]

    enroll_window = tk.Toplevel()
    enroll_window.title("Enroll Student in Subject")

    tk.Label(enroll_window, text="Student ID:").pack(pady=5)
    tk.Label(enroll_window, text=student_id).pack(pady=5)

    tk.Label(enroll_window, text="Select Subject:").pack(pady=5)
    subjects = fetch_subjects()
    subject_var = tk.StringVar(enroll_window)
    subject_menu = tk.OptionMenu(enroll_window, subject_var, *[subject[1] for subject in subjects])
    subject_menu.pack(pady=5)

    def enroll():
        selected_subject = subject_var.get()
        if selected_subject:
            enroll_student_in_subject(student_id, selected_subject)
            enroll_window.destroy()
        else:
            messagebox.showwarning("Error", "Please select a subject to enroll the student.")

    tk.Button(enroll_window, text="Enroll", command=enroll).pack(pady=10)

def view_enrolled_students_window(subjects_tree):
    selected_item = subjects_tree.focus()
    subject_code = subjects_tree.item(selected_item, "values")[0]

    enrolled_window = tk.Toplevel()
    enrolled_window.title(f"Enrolled Students for {subject_code}")

    tk.Label(enrolled_window, text=f"Students enrolled in Subject Code: {subject_code}").pack(pady=10)

    students_frame = tk.Frame(enrolled_window)
    students_frame.pack(fill="both", expand=True)

    columns = ("Student ID", "Student Name")
    enrolled_students_tree = ttk.Treeview(students_frame, columns=columns, show="headings")
    for col in columns:
        enrolled_students_tree.heading(col, text=col)
    enrolled_students_tree.pack(fill="both", expand=True)

    students = fetch_enrolled_students(subject_code)
    for student in students:
        enrolled_students_tree.insert("", tk.END, values=student)

    enrolled_students_tree.pack(pady=10, fill=tk.BOTH, expand=True)

def execute_query(query, params=(), commit=False):
    conn = sqlite3.connect('students_info.db')
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return results

# Run the function to create the table
create_enrollments_table()
