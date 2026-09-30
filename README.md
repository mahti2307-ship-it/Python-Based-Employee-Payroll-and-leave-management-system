# Payroll and Leave Management System

A desktop application built using **Python**, **Tkinter**, and **SQLite3**. This system provides a role-based workflow for managing employee records, processing monthly payrolls, and handling employee leave requests with an administrative panel and an employee portal.

---

## 🌟 Key Features

### 🔑 Authentication & Role-Based Access
- **Role Selection:** Main entry point allowing access to either **Admin** or **Employee** login portals.
- **Admin Portal:** Accessible with administrative credentials (Default: `admin` / `admin123`).
- **Employee Portal:** Accessible using an Employee ID and password (Default: `<emp_id>` / `emp123`).

### 👨‍💼 Admin Features
1. **Employee Management:**
   - Add new employees with detailed records (Name, Email, Department, Designation, Base Salary, Hourly Rate, Join Date).
   - Automatically generates default login credentials upon adding a new employee.
   - View registered employees in a structured table layout (`ttk.Treeview`).
2. **Leave Management:**
   - Review pending employee leave requests (Casual, Medical, Earned).
   - Approve or reject leave applications with real-time status updates.
3. **Payroll Processing:**
   - Auto-calculate payroll items:
     - **Overtime Pay:** $\text{Overtime Hours} \times \text{Hourly Rate}$
     - **Unpaid Leave Deductions:** $\left(\frac{\text{Base Salary}}{30}\right) \times \text{Unpaid Days}$
     - **Tax Deductions:** $10\%$ flat tax rate on Base Salary
     - **Net Salary:** $\text{Base} + \text{Overtime} - \text{Deductions} - \text{Tax}$
   - Store historical processed payslips in the database.

### 👷 Employee Features
- **Profile View:** Read-only access to personal employment and compensation details.
- **Leave Application:** Submit leave requests with custom date ranges and reasons.
- **Payslip History:** Track past leave request statuses and review processed monthly payslips.

---

## 🛠️️ Project Architecture

```text
payroll_system/
│
├── database.py      # SQLite schema initialization and connection handlers
├── auth.py          # Admin and Employee credential authentication logic
├── admin_gui.py     # Admin dashboard and management tab interfaces
├── employee_gui.py  # Employee self-service portal interface
├── main.py          # Application entry point and role routing GUI
├── .gitignore       # Untracked files filter (DB, cache, environment)
└── README.md        # Project documentation
