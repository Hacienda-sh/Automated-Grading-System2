import tkinter as tk
from tkinter import ttk, messagebox

from data_operations import fetch_subjects, fetch_enrolled_subjects
from enrollees_tab import enroll_student_in_subject, fetch_enrolled_students
from students_db import fetch_all_students, delete_student, fetch_student_by_id, update_student, add_student


def open_students_window(content_frame):
    """
    Opens the Students Management window in the content frame with search, view, edit, delete, add, and enroll functionalities.
    """
    # Clear existing content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Header
    tk.Label(content_frame, text="Students Management", font=("Arial", 16)).pack(pady=10)

    # Frame to hold the search bar
    search_frame = tk.Frame(content_frame)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search Student by ID:").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)

    def search_student():
        """Search and display a student by ID."""
        student_id = search_entry.get().strip()
        if not student_id:
            messagebox.showerror("Input Error", "Please enter a Student ID to search.")
            return

        student = fetch_student_by_id(student_id)
        students_tree.delete(*students_tree.get_children())  # Clear the Treeview

        if student:
            students_tree.insert("", tk.END, values=student)
        else:
            messagebox.showinfo("Not Found", f"No student found with ID: {student_id}")

    tk.Button(search_frame, text="Search", command=search_student).pack(side="left", padx=5)

    # Frame to hold the Treeview
    tree_frame = tk.Frame(content_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    # Treeview for displaying students
    columns = ("Student ID", "Last Name", "First Name", "Middle Name", "Curriculum", "Batch", "Course", "Sex",
               "Date of Birth", "Place of Birth", "Postal Address", "Home Phone Number", "Mobile Phone Number",
               "Email", "Residential Address", "Guardian Name", "Guardian Contact")
    students_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        students_tree.heading(col, text=col)
    students_tree.pack(fill="both", expand=True)

    # Populate Treeview with student data
    def load_students():
        students_tree.delete(*students_tree.get_children())
        students = fetch_all_students()
        for student in students:
            students_tree.insert("", tk.END, values=student)

    load_students()

    # Frame for action buttons
    action_frame = tk.Frame(content_frame)
    action_frame.pack(pady=10)

    def view_info():
        """View detailed info of the selected student."""
        selected_item = students_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to view.")
            return
        student_id = students_tree.item(selected_item)["values"][0]
        student = fetch_student_by_id(student_id)
        if student:
            info = "\n".join(f"{col}: {value}" for col, value in zip(columns, student))
            messagebox.showinfo("Student Info", info)
        else:
            messagebox.showerror("Error", "Student not found.")

    def edit_student():
        """Edit details of the selected student."""
        selected_item = students_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to edit.")
            return
        student_id = students_tree.item(selected_item)["values"][0]

        # Fetch current info
        student = fetch_student_by_id(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        # Open an edit form
        edit_window = tk.Toplevel()
        edit_window.title("Edit Student Info")

        entry_widgets = {}
        for i, col in enumerate(columns):
            tk.Label(edit_window, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, student[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_widgets[col] = entry

        def save_changes():
            new_values = {col: (entry.get().strip() if entry.get().strip() else "N/A") for col, entry in entry_widgets.items()}
            new_values["Student ID"] = student_id  # Keep Student ID unchanged

            if any(not value for value in new_values.values()):
                messagebox.showerror("Input Error", "All fields are required.")
                return

            if update_student(student_id, **new_values):
                messagebox.showinfo("Success", "Student info updated successfully.")
                load_students()
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update student info.")

        tk.Button(edit_window, text="Save", command=save_changes).grid(row=len(columns), columnspan=2, pady=10)

    def delete_student_action():
        """Delete the selected student."""
        selected_item = students_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return
        student_id = students_tree.item(selected_item)["values"][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            if delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully.")
                load_students()
            else:
                messagebox.showerror("Error", "Failed to delete student.")

    def prompt_add_student():
        """Open a window to add a new student."""
        add_window = tk.Toplevel()
        add_window.title("Add Student")

        entry_widgets = {}
        for i, col in enumerate(columns):
            tk.Label(add_window, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_widgets[col] = entry

        def add_student_action():
            new_student = {col: (entry.get().strip() if entry.get().strip() else "N/A") for col, entry in entry_widgets.items()}
            new_student["Student ID"] = entry_widgets["Student ID"].get().strip()
            new_student["Last Name"] = entry_widgets["Last Name"].get().strip()
            new_student["First Name"] = entry_widgets["First Name"].get().strip()
            if not new_student["Student ID"] or not new_student["Last Name"] or not new_student["First Name"]:
                messagebox.showerror("Input Error", "Student ID, Last Name, and First Name are required.")
                return

            add_student(
                student_id=new_student["Student ID"],
                last_name=new_student["Last Name"],
                first_name=new_student["First Name"],
                middle_name=new_student["Middle Name"],
                curriculum=new_student["Curriculum"],
                batch=new_student["Batch"],
                course=new_student["Course"],
                sex=new_student["Sex"],
                date_of_birth=new_student["Date of Birth"],
                place_of_birth=new_student["Place of Birth"],
                postal_address=new_student["Postal Address"],
                home_pnumber=new_student["Home Phone Number"],
                mobile_pnumber=new_student["Mobile Phone Number"],
                email=new_student["Email"],
                residential_address=new_student["Residential Address"],
                guardian_name=new_student["Guardian Name"],
                guardian_contact=new_student["Guardian Contact"]
            )
            messagebox.showinfo("Success", "Student added successfully.")
            load_students()
            add_window.destroy()

        tk.Button(add_window, text="Add", command=add_student_action).grid(row=len(columns), columnspan=2, pady=10)

    def enroll_student_action():
        """Enroll a student in a selected subject."""
        selected_item = students_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to enroll.")
            return
        student_id = students_tree.item(selected_item)["values"][0]

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

    def view_enrolled_subjects_action():
        """View subjects enrolled by the selected student."""
        selected_item = students_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to view enrolled subjects.")
            return
        student_id = students_tree.item(selected_item)["values"][0]

        enrolled_window = tk.Toplevel()
        enrolled_window.title("Enrolled Subjects")

        tk.Label(enrolled_window, text=f"Subjects enrolled by Student ID: {student_id}").pack(pady=10)

        subjects_frame = tk.Frame(enrolled_window)
        subjects_frame.pack(fill="both", expand=True)

        columns = ("Subject Code", "Subject Name")
        enrolled_subjects_tree = ttk.Treeview(subjects_frame, columns=columns, show="headings")
        for col in columns:
            enrolled_subjects_tree.heading(col, text=col)
        enrolled_subjects_tree.pack(fill="both", expand=True)

        subjects = fetch_enrolled_subjects(student_id)
        for subject in subjects:
            enrolled_subjects_tree.insert("", tk.END, values=subject)

        enrolled_subjects_tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Add action buttons
    tk.Button(action_frame, text="View Info", command=view_info).pack(side="left", padx=10)
    tk.Button(action_frame, text="Edit", command=edit_student).pack(side="left", padx=10)
    tk.Button(action_frame, text="Delete", command=delete_student_action).pack(side="left", padx=10)
    tk.Button(action_frame, text="Add Student", command=prompt_add_student).pack(side="left", padx=10)
    tk.Button(action_frame, text="Enroll in Subject", command=enroll_student_action).pack(side="left", padx=10)
    tk.Button(action_frame, text="View Enrolled Subjects", command=view_enrolled_subjects_action).pack(side="left", padx=10)


