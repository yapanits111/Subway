import sqlite3

def initialize_database():
    conn = sqlite3.connect('subwaydb.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applicant_info (
        emp_num INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_name TEXT,
        tax_ID_num TEXT,
        applicant_address TEXT,
        applicant_tel_num TEXT,
        age_verification TEXT,
        emergency_name TEXT,
        emergency_tel_num TEXT,
        emergency_address TEXT,
        position_type TEXT,
        total_hours INTEGER,
        date_availability TEXT,
        school_name TEXT,
        school_address TEXT,
        school_tel_num TEXT,
        counselor_name TEXT,
        grade_completed TEXT,
        GWA TEXT,
        graduated INTEGER,
        enrolled INTEGER
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment_history (
        history_code INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_num INTEGER,
        company_name TEXT,
        company_address TEXT,
        company_tel_num TEXT,
        position TEXT,
        supervisor TEXT,
        date_worked_from TEXT,
        date_worked_to TEXT,
        wage REAL,
        mgnt_ref_ck TEXT,
        reason_for_leaving TEXT,
        permission INTEGER,
        FOREIGN KEY(emp_num) REFERENCES applicant_info(emp_num)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reference (
        ref_code INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_num INTEGER,
        ref_name TEXT,
        ref_tel_num TEXT,
        years_known INTEGER,
        ref_address TEXT,
        FOREIGN KEY(emp_num) REFERENCES applicant_info(emp_num)
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully")
