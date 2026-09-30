import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class EmployeeDashboard(tk.Tk):
    def __init__(self, emp_id):
        super().__init__()
        self.emp_id = emp_id
        self.title(f"Employee Dashboard - ID #{self.emp_id}")
        self.geometry("750x500")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.profile_frame = ttk.Frame(self.notebook)
        self.apply_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.profile_frame, text="My Profile")
        self.notebook.add(self.apply_frame, text="Apply Leave")
        self.notebook.add(self.history_frame, text="Pay Slips")

        self.setup_profile()
        self.setup_apply()
        self.setup_history()

    # --- TAB 1: PROFILE ---
    def setup_profile(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, email, department, designation, base_salary FROM employees WHERE emp_id = ?", (self.emp_id,))
        emp = cursor.fetchone()
        conn.close()

        if emp:
            ttk.Label(self.profile_frame, text=f"Name: {emp[0]}", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=5)
            ttk.Label(self.profile_frame, text=f"Email: {emp[1]}").pack(anchor="w", padx=20, pady=5)
            ttk.Label(self.profile_frame, text=f"Department: {emp[2]}").pack(anchor="w", padx=20, pady=5)
            ttk.Label(self.profile_frame, text=f"Designation: {emp[3]}").pack(anchor="w", padx=20, pady=5)
            ttk.Label(self.profile_frame, text=f"Base Salary: ${emp[4]:.2f}").pack(anchor="w", padx=20, pady=5)

    # --- TAB 2: APPLY FOR LEAVE ---
    def setup_apply(self):
        ttk.Label(self.apply_frame, text="Leave Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.combo_type = ttk.Combobox(self.apply_frame, values=["Casual", "Medical", "Earned"])
        self.combo_type.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.apply_frame, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_start = ttk.Entry(self.apply_frame)
        self.ent_start.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.apply_frame, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ent_end = ttk.Entry(self.apply_frame)
        self.ent_end.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.apply_frame, text="Days Count:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ent_days = ttk.Entry(self.apply_frame)
        self.ent_days.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.apply_frame, text="Reason:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ent_reason = ttk.Entry(self.apply_frame)
        self.ent_reason.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(self.apply_frame, text="Submit Request", command=self.submit_leave).grid(row=5, column=1, pady=15, sticky="e")

    def submit_leave(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO leave_requests (emp_id, leave_type, start_date, end_date, days_count, reason)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.emp_id, self.combo_type.get(), self.ent_start.get(), self.ent_end.get(), int(self.ent_days.get()), self.ent_reason.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Submitted", "Leave request submitted for approval.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit: {e}")

    # --- TAB 3: PAYSLIP HISTORY ---
    def setup_history(self):
        tree = ttk.Treeview(self.history_frame, columns=("Month", "Base", "Overtime Pay", "Deductions", "Net Salary"), show="headings")
        for col in ("Month", "Base", "Overtime Pay", "Deductions", "Net Salary"):
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT month_year, base_salary, overtime_pay, (leave_deductions + tax_deductions), net_salary FROM payroll WHERE emp_id = ?", (self.emp_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    app = EmployeeDashboard(emp_id=1)
    app.mainloop()
