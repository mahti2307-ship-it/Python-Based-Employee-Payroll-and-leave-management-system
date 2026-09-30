from database import get_connection

def authenticate_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username FROM users WHERE username = ? AND password = ? AND role = 'Admin'",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_employee(emp_id, password=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if password:
        cursor.execute(
            "SELECT user_id, emp_id FROM users WHERE emp_id = ? AND password = ? AND role = 'Employee'",
            (emp_id, password)
        )
    else:
        cursor.execute(
            "SELECT emp_id, full_name FROM employees WHERE emp_id = ?",
            (emp_id,)
        )
    
    employee = cursor.fetchone()
    conn.close()
    return employee
