import streamlit as st
import sqlite3
import pandas as pd

def connect_db():
    return sqlite3.connect("subwaydb.db")
#ahahahahahah
def create_tables():
    with connect_db() as conn:
        conn.execute("""
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
                GWA REAL,
                graduated TEXT,
                enrolled TEXT
            )
        """)
        conn.execute("""
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
                wage TEXT,
                mgnt_ref_ck TEXT,
                reason_for_leaving TEXT,
                permission TEXT,
                FOREIGN KEY(emp_num) REFERENCES applicant_info(emp_num)
            )
        """)
        conn.execute("""
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


def create_applicant_info(empInfo):
    with connect_db() as conn:
        conn.execute("""
            INSERT INTO applicant_info (
                applicant_name, tax_ID_num, applicant_address, applicant_tel_num, age_verification,
                emergency_name, emergency_tel_num, emergency_address, position_type, total_hours,
                date_availability, school_name, school_address, school_tel_num, counselor_name,
                grade_completed, GWA, graduated, enrolled
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, empInfo)
        conn.commit()

def create_employment_history(employment_history):
    with connect_db() as conn:
        conn.execute("""
            INSERT INTO employment_history (
                emp_num, company_name, company_address, company_tel_num, position, supervisor,
                date_worked_from, date_worked_to, wage, mgnt_ref_ck, reason_for_leaving, permission
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, employment_history)
        conn.commit()

def create_reference(reference):
    with connect_db() as conn:
        conn.execute("""
            INSERT INTO reference (
                emp_num, ref_name, ref_tel_num, years_known, ref_address
            ) VALUES (?, ?, ?, ?, ?)
        """, reference)
        conn.commit()

def get_last_inserted_id():
    with connect_db() as conn:
        cursor = conn.execute("SELECT last_insert_rowid()")
        last_id = cursor.fetchone()
        return last_id[0] if last_id else None

def get_all_applicant_info():
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM applicant_info")
        data = cursor.fetchall()
        return data
    
def get_all_employment_history():
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM employment_history")
        data = cursor.fetchall()
        return data
        
def get_all_references():
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM reference")
        data = cursor.fetchall()
        return data

def update_data(emp_num, name, tax_id, address, phone):
    with connect_db() as conn:
        conn.execute("""
            UPDATE applicant_info
            SET applicant_name = ?, tax_ID_num = ?, applicant_address = ?, applicant_tel_num = ?
            WHERE emp_num = ?
        """, (name, tax_id, address, phone, emp_num))
        conn.commit()

def get_employment_history_by_emp_num(emp_num):
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM employment_history WHERE emp_num = ?", (emp_num,))
        employment_history = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in employment_history]

def update_employment_history(emp):
    with connect_db() as conn:
        conn.execute("""
            UPDATE employment_history
            SET company_name = ?, company_address = ?, company_tel_num = ?, position = ?, supervisor = ?, date_worked_from = ?, date_worked_to = ?, wage = ?, mgnt_ref_ck = ?, reason_for_leaving = ?, permission = ?
            WHERE emp_num = ? AND company_name = ?
        """, (
            emp['company_name'], emp['company_address'], emp['company_tel_num'], emp['position'], emp['supervisor'],
            emp['date_worked_from'], emp['date_worked_to'], emp['wage'], emp['mgnt_ref_ck'], emp['reason_for_leaving'],
            emp['permission'], emp['emp_num'], emp['company_name']
        ))
        conn.commit()

def get_references_by_emp_num(emp_num):
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM reference WHERE emp_num = ?", (emp_num,))
        references = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in references]

def update_reference(ref):
    with connect_db() as conn:
        conn.execute("""
            UPDATE reference
            SET ref_name = ?, ref_tel_num = ?, years_known = ?, ref_address = ?
            WHERE emp_num = ? AND ref_name = ?
        """, (
            ref['ref_name'], ref['ref_tel_num'], ref['years_known'], ref['ref_address'],
            ref['emp_num'], ref['ref_name']
        ))
        conn.commit()

def delete_data(emp_num):
    with connect_db() as conn:
        conn.execute("DELETE FROM applicant_info WHERE emp_num = ?", (emp_num,))
        conn.commit()