import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="subway"
    )

def create_user(email, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        emp_num = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return emp_num
    except Error as e:
        print(f"Error: {e}")
        return None

def get_user(email, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT emp_num FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    except Error as e:
        print(f"Error: {e}")
        return None

def get_applicant_info(emp_num):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM applicant_info WHERE emp_num=%s", (emp_num,))
        info = cursor.fetchone()
        cursor.close()
        connection.close()
        return info
    except Error as e:
        print(f"Error: {e}")
        return None

def update_applicant_info(data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            REPLACE INTO applicant_info (
                emp_num, applicant_name, tax_ID_num, applicant_address, applicant_tel_num, age_verification,
                emergency_name, emergency_tel_num, emergency_address, position_type, total_hours,
                date_availability, school_name, school_address, school_tel_num, counselor_name,
                grade_completed, GWA, graduated, enrolled
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

def get_employment_history(emp_num):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employment_history WHERE emp_num=%s", (emp_num,))
        history = cursor.fetchall()
        cursor.close()
        connection.close()
        return history
    except Error as e:
        print(f"Error: {e}")
        return None

def create_employment_history(emp_num, data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO employment_history (
                emp_num, company_name, company_address, company_tel_num, position, supervisor, date_worked_from,
                date_worked_to, wage, mgnt_ref_ck, reason_for_leaving, permission
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (emp_num, *data))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

def update_employment_history(history_code, data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE employment_history SET
                company_name=%s, company_address=%s, company_tel_num=%s, position=%s, supervisor=%s,
                date_worked_from=%s, date_worked_to=%s, wage=%s, mgnt_ref_ck=%s, reason_for_leaving=%s,
                permission=%s
            WHERE history_code=%s
        """, (*data, history_code))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

def get_references(emp_num):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reference WHERE emp_num=%s", (emp_num,))
        refs = cursor.fetchall()
        cursor.close()
        connection.close()
        return refs
    except Error as e:
        print(f"Error: {e}")
        return None

def create_reference(emp_num, data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO reference (
                emp_num, ref_name, ref_tel_num, years_known, ref_address
            ) VALUES (%s, %s, %s, %s, %s)
        """, (emp_num, *data))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

def update_reference(ref_code, data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE reference SET
                ref_name=%s, ref_tel_num=%s, years_known=%s, ref_address=%s
            WHERE ref_code=%s
        """, (*data, ref_code))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

def get_all_applicants():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM applicant_info")
        applicants = cursor.fetchall()
        cursor.close()
        connection.close()
        return applicants
    except Error as e:
        print(f"Error: {e}")
        return None

def update_application_status(emp_num, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET application_status=%s WHERE emp_num=%s", (status, emp_num))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")
