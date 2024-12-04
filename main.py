import tkinter as tk
from students_management import open_students_window
from record_management import open_records_window
from subjects import open_subjects_window
from students_db import setup_students_info_db
from rec_tab import setup_record_db
from sub_tab import setup_sub_db

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("Grading System")
        self.master.geometry("800x600")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        self.toggle_button = tk.Button(master, text="Hide Panel", command=self.toggle_side_panel)
        self.toggle_button.place(x=0, y=10, width=80)

        self.side_panel_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.side_panel_frame.pack(side="left", fill="y")

        self.label = tk.Label(self.side_panel_frame, text="Main Menu", bg="lightgray")
        self.label.pack(pady=20)

        # self.dashboard_button = tk.Button(self.side_panel_frame, text="Dashboard", command=self.create_dashboard)
        # self.dashboard_button.pack(pady=5)

        self.students_button = tk.Button(self.side_panel_frame, text="Students Management", command=self.open_students_window)
        self.students_button.pack(pady=5)

        self.records_button = tk.Button(self.side_panel_frame, text="Records Management", command=self.open_records_window)
        self.records_button.pack(pady=5)

        self.subjects_button = tk.Button(self.side_panel_frame, text="Subjects Management", command=self.open_subjects_window)
        self.subjects_button.pack(pady=5)

        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # self.create_dashboard()

    # def create_dashboard(self):
    #     self.clear_content_frame()
    #     tk.Label(self.content_frame, text="Welcome to the Grading System Dashboard", font=("Arial", 14)).pack()

    def open_students_window(self):
        self.clear_content_frame()
        open_students_window(self.content_frame)

    def open_records_window(self):
        self.clear_content_frame()
        open_records_window(self.content_frame)

    def open_subjects_window(self):
        self.clear_content_frame()
        open_subjects_window(self.content_frame)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def toggle_side_panel(self):
        if self.side_panel_frame.winfo_ismapped():
            self.side_panel_frame.pack_forget()
            self.toggle_button.config(text="Show Panel")
        else:
            self.side_panel_frame.pack(side="left", fill="y")
            self.toggle_button.config(text="Hide Panel")

# Ensure the databases are set up
setup_students_info_db()
setup_record_db()
setup_sub_db()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
