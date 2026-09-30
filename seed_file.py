import sqlite3
import random
from datetime import datetime, timedelta
from database import initialize_database, get_connection

def seed_database():
    # Ensure database structure exists
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data to avoid primary key conflicts
    cursor.execute("DELETE FROM payroll")
    cursor.execute("DELETE FROM leave_requests")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM employees")

    print("Cleared existing records...")

    # 1. INSERT HR / ADMIN ACCOUNTS
    admin_data = [
        ("hr_manager1", "hrpass123", "Admin"),
        ("hr_manager2", "hrpass456", "Admin"),
        ("admin", "admin123", "Admin")
    ]
    cursor.executemany("""
    INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    """, admin_data)

    print("Inserted HR Manager / Admin accounts...")

    # 2. GENERATE 100 EMPLOYEES DATA
    first_names = ["Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Sneha", "Aditya", "Kavya", 
                   "Rahul", "Neha", "Amit", "Pooja", "Siddharth", "Riya", "Karan", "Isha",
                   "Dev", "Simran", "Arjun", "Tanvi", "Manish", "Meera", "Varun", "Anjali"]
    
    last_names = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Reddy", "Joshi",
                  "Mehta", "Nair", "Rao", "Chopra", "Das", "Bhasin", "Deshmukh", "Agarwal"]

    departments = ["Engineering", "Human Resources", "Finance", "Marketing", "Sales", "Operations"]
    
    designations = {
        "Engineering": ["Software Engineer", "Senior Developer", "QA Specialist", "DevOps Engineer"],
        "Human Resources": ["HR Executive", "Talent Acquisition Lead", "HR Business Partner"],
        "Finance": ["Accountant", "Financial Analyst", "Audit Specialist"],
        "Marketing": ["Content Specialist", "Digital Marketer", "SEO Analyst"],
        "Sales": ["Sales Executive", "Account Manager", "Business Development Lead"],
        "Operations": ["Operations Associate", "Logistics Specialist", "Process Coordinator"]
    }

    start_date_range = datetime(2021, 1, 1)

    employees = []
    users = []

    used_emails = set()

    for i in range(1, 101):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        full_name = f"{fname} {lname}"
        
        email = f"{fname.lower()}.{lname.lower()}{i}@company.com"
        used_emails.add(email)

        dept = random.choice(departments)
        desig = random.choice(designations[dept])

        base_salary = round(random.uniform(35000, 120000), 2)
        hourly_rate = round(base_salary / 160, 2)  # Standard 160 hrs/month model

        # Random joining date over the last ~5 years
        random_days = random.randint(0, 1800)
        join_date = (start_date_range + timedelta(days=random_days)).strftime("%Y-%m-%d")

        employees.append((full_name, email, dept, desig, base_salary, hourly_rate, join_date))

    # Insert 100 Employees
    cursor.executemany("""
    INSERT INTO employees (full_name, email, department, designation, base_salary, hourly_rate, join_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, employees)

    # Map Employee ID to Users table (Username: emp_id, Password: emp123)
    cursor.execute("SELECT emp_id FROM employees")
    emp_ids = cursor.fetchall()

    for emp_tuple in emp_ids:
        e_id = emp_tuple[0]
        users.append((str(e_id), "emp123", "Employee", e_id))

    cursor.executemany("""
    INSERT INTO users (username, password, role, emp_id) VALUES (?, ?, ?, ?)
    """, users)

    print("Inserted 100 Employee profiles and login credentials...")

    # 3. GENERATE SAMPLE LEAVE REQUESTS
    leave_types = ["Casual", "Medical", "Earned"]
    statuses = ["Approved", "Pending", "Rejected"]

    leave_requests = []
    for _ in range(30):
        e_id = random.randint(1, 100)
        l_type = random.choice(leave_types)
        days = random.randint(1, 5)
        start = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
        end = (datetime.strptime(start, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")
        reason = f"Personal {l_type.lower()} requirement."
        status = random.choice(statuses)

        leave_requests.append((e_id, l_type, start, end, days, reason, status))

    cursor.executemany("""
    INSERT INTO leave_requests (emp_id, leave_type, start_date, end_date, days_count, reason, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, leave_requests)

    # 4. GENERATE SAMPLE PAYROLL RECORDS (FOR PREVIOUS MONTH)
    payroll_records = []
    cursor.execute("SELECT emp_id, base_salary, hourly_rate FROM employees LIMIT 25")
    sample_emps = cursor.fetchall()

    for emp in sample_emps:
        e_id, base_sal, h_rate = emp
        ot_hrs = random.choice([0, 5, 10, 15])
        unpaid_days = random.choice([0, 1, 2])
        
        ot_pay = ot_hrs * h_rate
        leave_ded = (base_sal / 30.0) * unpaid_days
        tax_ded = base_sal * 0.10
        net_sal = base_sal + ot_pay - leave_ded - tax_ded

        payroll_records.append((e_id, "08-2026", base_sal, ot_hrs, ot_pay, leave_ded, tax_ded, net_sal))

    cursor.executemany("""
    INSERT INTO payroll (emp_id, month_year, base_salary, overtime_hours, overtime_pay, leave_deductions, tax_deductions, net_salary)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, payroll_records)

    conn.commit()
    conn.close()

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
