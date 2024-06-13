import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='subway',
            user='root',
            password='password'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_user(username, password, email):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    connection.commit()
    cursor.close()
    connection.close()

def get_user(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def fetch_applicant_info(username):
    query = "SELECT * FROM applicants WHERE username = %s"
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (username,))
            applicant_data = cursor.fetchone()
            return applicant_data  # Return fetched data
        except Error as e:
            print(f"Error fetching applicant data: {e}")
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            connection.close()
    return None  # Return None if no data found or error occurred

def add_applicant_info(applicant_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO applicants (username, applicant_name, tax_ID_num, applicant_address, applicant_tel_num, age_verification, emergency_name, emergency_tel_num, emergency_address, position_type, total_hours, date_availability, school_name, school_address, school_tel_num, counselor_name, grade_completed, GWA, graduated, enrolled)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        applicant_data["username"],
        applicant_data["applicant_name"],
        applicant_data["tax_ID_num"],
        applicant_data["applicant_address"],
        applicant_data["applicant_tel_num"],
        applicant_data["age_verification"],
        applicant_data["emergency_name"],
        applicant_data["emergency_tel_num"],
        applicant_data["emergency_address"],
        applicant_data["position_type"],
        applicant_data["total_hours"],
        applicant_data["date_availability"],
        applicant_data["school_name"],
        applicant_data["school_address"],
        applicant_data["school_tel_num"],
        applicant_data["counselor_name"],
        applicant_data["grade_completed"],
        applicant_data["GWA"],
        applicant_data["graduated"],
        applicant_data["enrolled"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def update_applicant_info(applicant_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    UPDATE applicants
    SET applicant_name = %s, tax_ID_num = %s, applicant_address = %s, applicant_tel_num = %s, age_verification = %s, emergency_name = %s, emergency_tel_num = %s, emergency_address = %s, position_type = %s, total_hours = %s, date_availability = %s, school_name = %s, school_address = %s, school_tel_num = %s, counselor_name = %s, grade_completed = %s, GWA = %s, graduated = %s, enrolled = %s
    WHERE username = %s
    """
    cursor.execute(query, (
        applicant_data["applicant_name"],
        applicant_data["tax_ID_num"],
        applicant_data["applicant_address"],
        applicant_data["applicant_tel_num"],
        applicant_data["age_verification"],
        applicant_data["emergency_name"],
        applicant_data["emergency_tel_num"],
        applicant_data["emergency_address"],
        applicant_data["position_type"],
        applicant_data["total_hours"],
        applicant_data["date_availability"],
        applicant_data["school_name"],
        applicant_data["school_address"],
        applicant_data["school_tel_num"],
        applicant_data["counselor_name"],
        applicant_data["grade_completed"],
        applicant_data["GWA"],
        applicant_data["graduated"],
        applicant_data["enrolled"],
        applicant_data["username"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def fetch_employment_history(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM employment_history WHERE username = %s"
    cursor.execute(query, (username,))
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    return history

def add_employment_history(history_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO employment_history (username, company_name, company_address, company_tel_num, position, supervisor, date_worked_from, date_worked_to, wage, mgnt_ref_ck, reason_for_leaving, permission)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        history_data["username"],
        history_data["company_name"],
        history_data["company_address"],
        history_data["company_tel_num"],
        history_data["position"],
        history_data["supervisor"],
        history_data["date_worked_from"],
        history_data["date_worked_to"],
        history_data["wage"],
        history_data["mgnt_ref_ck"],
        history_data["reason_for_leaving"],
        history_data["permission"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def fetch_references(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM reference WHERE username = %s"
    cursor.execute(query, (username,))
    references = cursor.fetchall()
    cursor.close()
    connection.close()
    return references

def add_reference(ref_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO reference (username, ref_name, ref_tel_num, years_known, ref_address)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        ref_data["username"],
        ref_data["ref_name"],
        ref_data["ref_tel_num"],
        ref_data["years_known"],
        ref_data["ref_address"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def fetch_all_applicants():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM applicants"
    cursor.execute(query)
    applicants = cursor.fetchall()
    cursor.close()
    connection.close()
    return applicants
