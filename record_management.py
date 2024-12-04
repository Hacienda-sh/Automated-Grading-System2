import tkinter as tk
from tkinter import ttk
import sqlite3
from data_operations import fetch_subjects, fetch_student_names, update_grade
from calc_new_curriculum import ComputationNewCurriculum
from calc_old_curriculum import ComputationOldCurriculum
from spreadsheet import show_performance_based_activities


def open_records_window(content_frame):
    # Clear existing content
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Records Management", font=("Arial", 16)).pack(pady=10)

    tree_frame = tk.Frame(content_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("Sub Code", "Subject Name", "Semester")
    records_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        records_tree.heading(col, text=col)
    records_tree.pack(fill="both", expand=True)

    load_records(records_tree)
    records_tree.bind("<Double-1>", lambda e: open_grades_spreadsheet(e, records_tree))

    records_tree.pack(pady=10, fill=tk.BOTH, expand=True)

def load_records(records_tree):
    records_tree.delete(*records_tree.get_children())

    conn = sqlite3.connect('students_info.db')
    cur = conn.cursor()
    cur.execute("SELECT sub_code, name, semester FROM subjects")
    records = cur.fetchall()
    conn.close()

    for record in records:
        sub_code, subject_name, semester = record
        records_tree.insert("", tk.END, values=(sub_code, subject_name, semester))

def open_grades_spreadsheet(event, tree):
    selected_item = tree.selection()[0]
    subject_code = tree.item(selected_item, "values")[0]
    global selected_subject_code
    selected_subject_code = subject_code

    global grades_window
    grades_window = tk.Toplevel()
    grades_window.title(f"Grades for {subject_code}")
    grades_window.geometry("800x600")

    global period_frame
    period_frame = tk.Frame(grades_window)
    period_frame.pack(pady=10)

    tk.Label(period_frame, text="Select Period:").pack(side="left", padx=5)
    global period_var
    period_var = tk.StringVar(period_frame)
    period_var.set("Midterms")
    periods = ["Midterms", "Finals"]
    period_menu = tk.OptionMenu(period_frame, period_var, *periods)
    period_menu.pack(side="left", padx=5)

    global input_frame
    input_frame = tk.Frame(grades_window)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Select Assessment Type:").pack(side="left", padx=5)
    global assessment_type_var
    assessment_type_var = tk.StringVar(input_frame)
    assessment_type_var.set("Exam")
    assessment_types = ["Exam", "Quiz", "Performance-Based Activities"]
    assessment_type_menu = tk.OptionMenu(input_frame, assessment_type_var, *assessment_types)
    assessment_type_menu.pack(side="left", padx=5)

    period_var.trace("w", update_spreadsheet)
    assessment_type_var.trace("w", update_spreadsheet)

    global performance_frame
    performance_frame = tk.Frame(grades_window)
    performance_frame.pack_forget()

def update_spreadsheet(*args):
    period = period_var.get()
    assessment_type = assessment_type_var.get()
    subject_code = selected_subject_code

    for widget in grades_window.winfo_children():
        if isinstance(widget, tk.Frame) and widget not in [period_frame, input_frame, performance_frame]:
            widget.destroy()

    if assessment_type == "Performance-Based Activities":
        show_performance_based_activities(grades_window, subject_code, period)
    else:
        show_standard_assessment(grades_window, subject_code, period, assessment_type)

def show_standard_assessment(parent, subject_code, period, assessment_type):
    tree_frame = tk.Frame(parent)
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    columns = ("Name", assessment_type)
    grades_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        grades_tree.heading(col, text=col)
    grades_tree.pack(fill="both", expand=True)

    highest_score_frame = tk.Frame(parent)
    highest_score_frame.pack(pady=10)
    tk.Label(highest_score_frame, text=f"Enter Highest Possible Score for {period} {assessment_type}:").pack(side="left", padx=5)
    highest_score_entry = tk.Entry(highest_score_frame)
    highest_score_entry.pack(side="left", padx=5)

    student_names = fetch_student_names(subject_code)

    for student in student_names:
        student_id, student_name = student
        grades_tree.insert("", tk.END, values=(student_name, ""))

    grades_tree.bind("<Double-1>", lambda e: edit_grade_cell(e, grades_tree, subject_code, period, assessment_type, highest_score_entry))

def edit_grade_cell(event, tree, subject_code, period, assessment_type, highest_score_entry):
    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if not row_id or not column_id:
        return

    selected_item = tree.item(row_id)
    col_index = int(column_id[1:]) - 1
    old_value = selected_item["values"][col_index]

    entry = tk.Entry(tree)
    entry.insert(0, old_value)
    entry.place(x=tree.bbox(row_id, column_id)[0], y=tree.bbox(row_id, column_id)[1])

    def save_new_value(event):
        new_value = entry.get()
        entry.destroy()
        selected_item["values"] = list(selected_item["values"])
        selected_item["values"][col_index] = new_value
        tree.item(row_id, values=selected_item["values"])

        student_name = selected_item["values"][0]
        conn = sqlite3.connect('students_info.db')
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE first_name || ' ' || last_name = ?", (student_name,))
        student_id = cur.fetchone()[0]
        conn.close()

        update_grade(student_id, subject_code, assessment_type.lower(), new_value, period)

        conn = sqlite3.connect('students_info.db')
        cur = conn.cursor()
        cur.execute(f"""
            SELECT quiz, midterm_exam, final_exam, participation, assignments 
            FROM grades WHERE student_id = ? AND subject_code = ? AND period = ?
        """, (student_id, subject_code, period))
        updated_grades = cur.fetchone()
        conn.close()

        highest_score = float(highest_score_entry.get())
        score_percentage = (float(new_value) / highest_score) * 100

        if selected_item["values"][2] == 'new':
            final_grade = ComputationNewCurriculum.calculate_semestral_grade(updated_grades[1], updated_grades[3], score_percentage)
        else:
            final_grade = ComputationOldCurriculum.calculate_semestral_grade(updated_grades[1], updated_grades[3], score_percentage)

        update_grade(student_id, subject_code, "final_grade", final_grade, period)

    entry.bind("<Return>", save_new_value)
    entry.focus()
