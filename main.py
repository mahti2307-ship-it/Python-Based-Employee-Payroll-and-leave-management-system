import tkinter as tk
from tkinter import ttk, messagebox
from database import initialize_database
from auth import authenticate_admin, authenticate_employee
from admin_gui import AdminDashboard
from employee_gui import EmployeeDashboard

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Payroll System - Role Selection")
        self.geometry("400x300")

        # Ensure database tables are created on launch
        initialize_database()

        ttk.Label(self, text="Select User Role", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Button(self, text="Admin Login", width=25, command=self.open_admin_login).pack(pady=10)
        ttk.Button(self, text="Employee Login", width=25, command=self.open_employee_login).pack(pady=10)

    def open_admin_login(self):
        LoginWindow(self, role="Admin")

    def open_employee_login(self):
        LoginWindow(self, role="Employee")


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, role):
        super().__init__(parent)
        self.parent = parent
        self.role = role
        self.title(f"{role} Authentication")
        self.geometry("350x250")

        ttk.Label(self, text=f"{role} Login Panel", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self, text="Username / ID:").pack(anchor="w", padx=30)
        self.ent_user = ttk.Entry(self)
        self.ent_user.pack(fill="x", padx=30, pady=5)

        ttk.Label(self, text="Password:").pack(anchor="w", padx=30)
        self.ent_pass = ttk.Entry(self, show="*")
        self.ent_pass.pack(fill="x", padx=30, pady=5)

        ttk.Button(self, text="Login", command=self.handle_login).pack(pady=15)

    def handle_login(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()

        if self.role == "Admin":
            user = authenticate_admin(username, password)
            if user:
                messagebox.showinfo("Success", "Welcome, Admin!")
                self.destroy()
                self.parent.destroy()
                app = AdminDashboard()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Admin credentials.")
        else:
            try:
                emp_id = int(username)
                employee = authenticate_employee(emp_id, password)
                if employee:
                    messagebox.showinfo("Success", f"Welcome Employee #{emp_id}")
                    self.destroy()
                    self.parent.destroy()
                    app = EmployeeDashboard(emp_id=emp_id)
                    app.mainloop()
                else:
                    messagebox.showerror("Error", "Invalid Employee credentials.")
            except ValueError:
                messagebox.showerror("Error", "Employee ID must be an integer.")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
