import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import get_connection

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Payroll System - Admin Dashboard")
        self.geometry("900x650")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.emp_frame = ttk.Frame(self.notebook)
        self.leave_frame = ttk.Frame(self.notebook)
        self.payroll_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.emp_frame, text="Employee Management")
        self.notebook.add(self.leave_frame, text="Leave Requests")
        self.notebook.add(self.payroll_frame, text="Payroll Processing")

        self.setup_employee_tab()
        self.setup_leave_tab()
        self.setup_payroll_tab()

    # --- TAB 1: EMPLOYEE MANAGEMENT ---
    def setup_employee_tab(self):
        form_frame = ttk.LabelFrame(self.emp_frame, text=" Add New Employee ")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_name = ttk.Entry(form_frame)
        self.ent_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_email = ttk.Entry(form_frame)
        self.ent_email.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Department:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_dept = ttk.Entry(form_frame)
        self.ent_dept.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Designation:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ent_desig = ttk.Entry(form_frame)
        self.ent_desig.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Base Salary:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_salary = ttk.Entry(form_frame)
        self.ent_salary.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Hourly Rate:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.ent_rate = ttk.Entry(form_frame)
        self.ent_rate.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Join Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_date = ttk.Entry(form_frame)
        self.ent_date.grid(row=3, column=1, padx=5, pady=5)

        btn_add = ttk.Button(form_frame, text="Save Employee", command=self.add_employee)
        btn_add.grid(row=3, column=3, padx=5, pady=5, sticky="e")

        # Treeview Table
        tree_frame = ttk.Frame(self.emp_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.emp_tree = ttk.Treeview(
            tree_frame, 
            columns=("ID", "Name", "Email", "Department", "Designation", "Base Salary"), 
            show="headings"
        )
        for col in ("ID", "Name", "Email", "Department", "Designation", "Base Salary"):
            self.emp_tree.heading(col, text=col)
            self.emp_tree.column(col, width=120)

        self.emp_tree.pack(fill="both", expand=True)
        self.load_employees()

    def add_employee(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Insert Employee Record
            cursor.execute("""
            INSERT INTO employees (full_name, email, department, designation, base_salary, hourly_rate, join_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.ent_name.get(), self.ent_email.get(), self.ent_dept.get(),
                self.ent_desig.get(), float(self.ent_salary.get()),
                float(self.ent_rate.get()), self.ent_date.get()
            ))
            
            emp_id = cursor.lastrowid
            
            # Auto-generate default login credentials for Employee (Username: emp_id, Pass: emp123)
            cursor.execute("""
            INSERT INTO users (username, password, role, emp_id)
            VALUES (?, ?, 'Employee', ?)
            """, (str(emp_id), "emp123", emp_id))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Employee added successfully! Login ID is {emp_id}")
            self.load_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {e}")

    def load_employees(self):
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, full_name, email, department, designation, base_salary FROM employees")
        for row in cursor.fetchall():
            self.emp_tree.insert("", "end", values=row)
        conn.close()

    # --- TAB 2: LEAVE MANAGEMENT ---
    def setup_leave_tab(self):
        self.leave_tree = ttk.Treeview(
            self.leave_frame, 
            columns=("Leave ID", "Emp ID", "Type", "Start", "End", "Days", "Reason", "Status"), 
            show="headings"
        )
        for col in ("Leave ID", "Emp ID", "Type", "Start", "End", "Days", "Reason", "Status"):
            self.leave_tree.heading(col, text=col)
            self.leave_tree.column(col, width=100)

        self.leave_tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.leave_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Approve", command=lambda: self.update_leave("Approved")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Reject", command=lambda: self.update_leave("Rejected")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_leaves).pack(side="right", padx=5)

        self.load_leaves()

    def load_leaves(self):
        for item in self.leave_tree.get_children():
            self.leave_tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT leave_id, emp_id, leave_type, start_date, end_date, days_count, reason, status FROM leave_requests")
        for row in cursor.fetchall():
            self.leave_tree.insert("", "end", values=row)
        conn.close()

    def update_leave(self, status):
        selected = self.leave_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request.")
            return
        leave_id = self.leave_tree.item(selected[0])['values'][0]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE leave_requests SET status = ? WHERE leave_id = ?", (status, leave_id))
        conn.commit()
        conn.close()
        self.load_leaves()

    # --- TAB 3: PAYROLL PROCESSING ---
    def setup_payroll_tab(self):
        frame = ttk.LabelFrame(self.payroll_frame, text=" Process Monthly Payroll ")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Emp ID:").grid(row=0, column=0, padx=5, pady=5)
        self.p_empid = ttk.Entry(frame)
        self.p_empid.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Month-Year (MM-YYYY):").grid(row=0, column=2, padx=5, pady=5)
        self.p_month = ttk.Entry(frame)
        self.p_month.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Overtime Hours:").grid(row=1, column=0, padx=5, pady=5)
        self.p_ot = ttk.Entry(frame)
        self.p_ot.insert(0, "0")
        self.p_ot.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Unpaid Leave Days:").grid(row=1, column=2, padx=5, pady=5)
        self.p_leaves = ttk.Entry(frame)
        self.p_leaves.insert(0, "0")
        self.p_leaves.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Calculate & Process", command=self.process_payroll).grid(row=2, column=3, padx=5, pady=10)

    def process_payroll(self):
        try:
            emp_id = int(self.p_empid.get())
            month = self.p_month.get()
            ot_hours = float(self.p_ot.get())
            unpaid_days = float(self.p_leaves.get())

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT base_salary, hourly_rate FROM employees WHERE emp_id = ?", (emp_id,))
            emp = cursor.fetchone()

            if not emp:
                messagebox.showerror("Error", "Employee ID not found.")
                conn.close()
                return

            base_sal, h_rate = emp[0], emp[1]
            ot_pay = ot_hours * h_rate
            leave_ded = (base_sal / 30.0) * unpaid_days
            tax_ded = base_sal * 0.10  # 10% Flat Tax
            net_sal = base_sal + ot_pay - leave_ded - tax_ded

            cursor.execute("""
            INSERT INTO payroll (emp_id, month_year, base_salary, overtime_hours, overtime_pay, leave_deductions, tax_deductions, net_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (emp_id, month, base_sal, ot_hours, ot_pay, leave_ded, tax_ded, net_sal))

            conn.commit()
            conn.close()
            messagebox.showinfo("Payroll Processed", f"Net Salary Processed: ${net_sal:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid parameters: {e}")

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
