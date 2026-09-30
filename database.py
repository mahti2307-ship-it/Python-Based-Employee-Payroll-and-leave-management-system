import sqlite3

DB_NAME = "payroll_system.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        designation TEXT NOT NULL,
        base_salary REAL NOT NULL,
        hourly_rate REAL NOT NULL,
        join_date TEXT NOT NULL
    );
    """)

    # Users / Auth Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        emp_id INTEGER,
        FOREIGN KEY (emp_id) REFERENCES employees (emp_id) ON DELETE CASCADE
    );
    """)

    # Leave Requests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER NOT NULL,
        leave_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        days_count INTEGER NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (emp_id) REFERENCES employees (emp_id) ON DELETE CASCADE
    );
    """)

    # Payroll Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER NOT NULL,
        month_year TEXT NOT NULL,
        base_salary REAL NOT NULL,
        overtime_hours REAL DEFAULT 0,
        overtime_pay REAL DEFAULT 0,
        leave_deductions REAL DEFAULT 0,
        tax_deductions REAL DEFAULT 0,
        net_salary REAL NOT NULL,
        FOREIGN KEY (emp_id) REFERENCES employees (emp_id) ON DELETE CASCADE
    );
    """)

    # Insert default Admin if not exists
    cursor.execute("SELECT * FROM users WHERE role = 'Admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password, role) 
        VALUES ('admin', 'admin123', 'Admin')
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
