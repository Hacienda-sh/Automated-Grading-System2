import tkinter as tk
from tkinter import messagebox, ttk
from sub_tab import add_subject, fetch_all_subjects, delete_subject, save_grading_criteria

def open_subjects_window(content_frame):
    """
    Opens the Subjects Management window in the content frame with functionalities to add, delete, and edit subjects.
    """
    # Clear existing content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Header
    tk.Label(content_frame, text="Subjects Management", font=("Arial", 16)).pack(pady=10)

    # Frame to hold the Treeview for displaying subjects
    tree_frame = tk.Frame(content_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    columns = ("Subject Name", "Course Code", "Semester")
    subjects_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        subjects_tree.heading(col, text=col)
    subjects_tree.pack(fill="both", expand=True)

    # Frame to hold the action buttons
    action_frame = tk.Frame(content_frame)
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="Add Subject", command=lambda: prompt_add_subject(subjects_tree)).pack(side="left", padx=10)
    tk.Button(action_frame, text="Delete Subject", command=lambda: prompt_delete_subject(subjects_tree)).pack(side="left", padx=10)
    tk.Button(action_frame, text="Edit Subject", command=lambda: prompt_edit_subject(subjects_tree)).pack(side="left", padx=10)

    # Load and display subjects
    load_subjects(subjects_tree)
    # Display the Treeview
    subjects_tree.pack(pady=10, fill=tk.BOTH, expand=True)

def load_subjects(subjects_tree):
    # Clear existing subjects in the Treeview before adding new ones
    subjects_tree.delete(*subjects_tree.get_children())

    # Fetch subjects from the database
    subjects = fetch_all_subjects()
    for subject in subjects:
        subject_name, course_code, semester = subject
        subjects_tree.insert("", tk.END, values=(subject_name, course_code, semester))

def prompt_add_subject(subjects_tree):
    add_subject_window = tk.Toplevel()
    add_subject_window.title("Add Subject")

    tk.Label(add_subject_window, text="Enter Subject Name:").pack(pady=5)
    subject_name_entry = tk.Entry(add_subject_window)
    subject_name_entry.pack(pady=5)

    tk.Label(add_subject_window, text="Enter Course Code:").pack(pady=5)
    course_code_entry = tk.Entry(add_subject_window)
    course_code_entry.pack(pady=5)

    semester_var = tk.StringVar(add_subject_window)
    semester_var.set("1st Year - 1st Semester")
    semester_options = ["1st Year - 1st Semester", "1st Year - 2nd Semester", "2nd Year - 1st Semester", "2nd Year - 2nd Semester"]
    tk.Label(add_subject_window, text="Select Semester:").pack(pady=5)
    semester_dropdown = tk.OptionMenu(add_subject_window, semester_var, *semester_options)
    semester_dropdown.pack(pady=5)

    def add():
        subject_name = subject_name_entry.get().strip()
        course_code = course_code_entry.get().strip()
        semester = semester_var.get()
        if subject_name and course_code and semester:
            add_subject(subject_name, course_code, semester)
            load_subjects(subjects_tree)
            add_subject_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter subject name, course code, and select a semester.")

    tk.Button(add_subject_window, text="Add", command=add).pack(pady=10)

def prompt_edit_subject(subjects_tree):
    selected_item = subjects_tree.focus()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a subject to edit.")
        return

    subject_name = subjects_tree.item(selected_item, "values")[0]
    edit_grading_criteria(subject_name)

def edit_grading_criteria(subject_name):
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Grading Criteria for {subject_name}")

    tk.Label(edit_window, text=f"Edit Grading Criteria for {subject_name}").pack(pady=10)

    tk.Label(edit_window, text="Exam Weight (%)").grid(row=0, column=0, padx=10, pady=5)
    exam_weight_entry = tk.Entry(edit_window)
    exam_weight_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Project Weight (%)").grid(row=1, column=0, padx=10, pady=5)
    project_weight_entry = tk.Entry(edit_window)
    project_weight_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Quiz Weight (%)").grid(row=2, column=0, padx=10, pady=5)
    quiz_weight_entry = tk.Entry(edit_window)
    quiz_weight_entry.grid(row=2, column=1, padx=10, pady=5)

    def save():
        try:
            exams_weight = float(exam_weight_entry.get())
            projects_weight = float(project_weight_entry.get())
            quizzes_weight = float(quiz_weight_entry.get())

            if exams_weight + projects_weight + quizzes_weight != 100:
                messagebox.showerror("Error", "Total weight must equal 100%.")
                return

            save_grading_criteria(subject_name, exams_weight, projects_weight, quizzes_weight)
            messagebox.showinfo("Success", "Grading criteria saved successfully!")
            edit_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weights.")

    tk.Button(edit_window, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=10)

def prompt_delete_subject(subjects_tree):
    selected_item = subjects_tree.focus()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a subject to delete.")
        return

    course_code = subjects_tree.item(selected_item, "values")[1]
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the subject with course code '{course_code}'?"):
        delete_subject(course_code)
        load_subjects(subjects_tree)

if __name__ == "__main__":
    root = tk.Tk()
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)
    open_subjects_window(content_frame)
    root.mainloop()
