import streamlit as st
import pandas as pd
from db_functions import *

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.session_state['logged_in'] = True
    st.success("Logged in successfully!")

def logout():
    st.session_state['logged_in'] = False
    st.success("Logged out successfully!")

def admin_login():
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if username == 'admin' and password == 'pass':
            login()
        else:
            st.error("Incorrect username or password")

def admin_panel():
    if not st.session_state['logged_in']:
        admin_login()
        return
    else:
        st.write("Welcome, admin! You are logged in.")
        if st.button("Logout"):
            logout()

    st.subheader("Admin Panel")
    t1 = get_all_applicant_info()
    df1 = pd.DataFrame(t1, columns=["Employee Number", "Name", "Tax ID", "Address", "Phone", "Age Verification", "Emergency Name", "Emergency Phone", "Emergency Address", "Position Type", "Hours", "Start Date", "School", "School Address", "School Phone", "Counselor", "Grade", "GWA", "Graduated", "Enrolled"])
    
    t2 = get_all_employment_history()
    df2 = pd.DataFrame(t2, columns=["History Code", "Employee Number", "Company Name", "Company Address", "Company Phone", "Position", "Supervisor", "Start Date", "End Date", "Wage", "Management Reference Checked By", "Reason For Leaving", "Permission to Contact"])
    
    t3 = get_all_references()
    df3 = pd.DataFrame(t3, columns=["Reference Code", "Employee Number", "Name", "Contact Number", "Years Known", "Address"])

    st.write("Employee Information")
    st.dataframe(df1)
    st.write("Employment Histories")
    st.dataframe(df2)
    st.write("References")
    st.dataframe(df3)

    selected_id = st.text_input("Enter Employment Number to update/delete:")
    selected_row = df1[df1["Employee Number"] == int(selected_id)] if selected_id else pd.DataFrame()

    if st.button("Search"):
        if not selected_row.empty:
            st.write("Update Applicant Information")

            st.subheader("*I. Personal Information*")
            updated_name = st.text_input("Full Name", value=selected_row["Name"].values[0])
            updated_tax_id = st.text_input("Tax ID Number", value=selected_row["Tax ID"].values[0])
            updated_address = st.text_input("Address", value=selected_row["Address"].values[0])
            updated_tel_num = st.text_input("Phone Number", value=selected_row["Phone"].values[0])
            updated_age_verification = st.radio("16 Years or above?", ["Yes", "No"], index=0 if selected_row["Age Verification"].values[0] == "Yes" else 1)
        
            st.subheader("*II. Emergency Contact*")
            updated_emergency_name = st.text_input("Emergency Contact Name", value=selected_row["Emergency Name"].values[0])
            updated_emergency_tel_num = st.text_input("Emergency Contact Number", value=selected_row["Emergency Phone"].values[0])
            updated_emergency_address = st.text_input("Contact Address", value=selected_row["Emergency Address"].values[0])

            st.subheader("*III. Availability*")
            updated_position_type = st.radio("Position Type", ["Part Time", "Full Time", "Seasonal", "Temporary"], index=0)
            updated_total_hours = st.number_input("Total Hours Available Per Week", min_value=0, value=selected_row["Hours"].values[0])
            updated_date_availability = st.date_input("Date Available to Start Work", value=pd.to_datetime(selected_row["Start Date"].values[0]))
        
            st.subheader("*IV. School Most Recent Attended*")
            updated_school_name = st.text_input("School Name", value=selected_row["School"].values[0])
            updated_school_address = st.text_input("School Address", value=selected_row["School Address"].values[0])
            updated_school_tel_num = st.text_input("School Telephone Number", value=selected_row["School Phone"].values[0])
            updated_counselor_name = st.text_input("Counselor Name", value=selected_row["Counselor"].values[0])
            updated_grade_completed = st.radio("Last Grade Completed", ['Elementary', 'Junior High School', 'Senior High School', 'College'], index=['Elementary', 'Junior High School', 'Senior High School', 'College'].index(selected_row["Grade"].values[0]), horizontal=True)
            updated_GWA = st.number_input("Most Recent GWA", value=selected_row["GWA"].values[0])
            updated_graduated = st.radio("Graduated?", ["Yes", "No"], index=0 if selected_row["Graduated"].values[0] == "Yes" else 1)
            updated_enrolled = st.radio("Currently Enrolled?", ["Yes", "No"], index=0 if selected_row["Enrolled"].values[0] == "Yes" else 1)

        """st.subheader("Update Employment History")
        employment_history = get_employment_history_by_emp_num(int(selected_id))
        if employment_history:
            for i, emp in enumerate(employment_history):
                st.write(f"Employment History {i+1}")
                emp['company_name'] = st.text_input(f"Company Name {i+1}", value=emp['company_name'])
                emp['company_address'] = st.text_input(f"Company Address {i+1}", value=emp['company_address'])
                emp['company_tel_num'] = st.text_input(f"Company Telephone Number {i+1}", value=emp['company_tel_num'])
                emp['position'] = st.text_input(f"Position {i+1}", value=emp['position'])
                emp['supervisor'] = st.text_input(f"Supervisor {i+1}", value=emp['supervisor'])
                emp['date_worked_from'] = st.date_input(f"Date Worked From {i+1}", value=pd.to_datetime(emp['date_worked_from']))
                emp['date_worked_to'] = st.date_input(f"Date Worked To {i+1}", value=pd.to_datetime(emp['date_worked_to']))
                emp['wage'] = st.text_input(f"Wage {i+1}", value=emp['wage'])
                emp['mgnt_ref_ck'] = st.text_input(f"Management Reference Checked By {i+1}", value=emp['mgnt_ref_ck'])
                emp['reason_for_leaving'] = st.text_input(f"Reason for Leaving {i+1}", value=emp['reason_for_leaving'])
                emp['permission'] = st.radio(f"Do we have your permission to contact your previous employer? {i+1}", ['Yes', 'No'], index=0 if emp['permission'] == "Yes" else 1)

        st.subheader("Update References")
        references = get_references_by_emp_num(int(selected_id))
        if references:
            for j, ref in enumerate(references):
                st.write(f"Reference Person {j+1}")
                ref['ref_name'] = st.text_input(f"Full Name {j+1}", value=ref['ref_name'])
                ref['ref_tel_num'] = st.text_input(f"Tel. Number {j+1}", value=ref['ref_tel_num'])
                ref['years_known'] = st.number_input(f"Years Known {j+1}", value=ref['years_known'], min_value=0)
                ref['ref_address'] = st.text_input(f"Home Address {j+1}", value=ref['ref_address'])"""

        if st.button("Update"):
            try:
                update_data(int(selected_id), updated_name, updated_tax_id, updated_address, updated_tel_num, updated_age_verification, updated_emergency_name, updated_emergency_tel_num, updated_emergency_address, updated_position_type, updated_total_hours, updated_date_availability, updated_school_name, updated_school_address, updated_school_tel_num, updated_counselor_name, updated_grade_completed, updated_GWA, updated_graduated, updated_enrolled)

                """if employment_history:
                    for emp in employment_history:
                        update_employment_history(emp)

                if references:
                    for ref in references:
                        update_reference(ref)"""

                st.success("Record updated successfully")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        if st.button("Delete"):
            try:
                delete_data(int(selected_id))
                st.success("Record deleted successfully")
            except Exception as e:
                st.error(f"An error occurred: {e}")

def main():
    if st.session_state['logged_in']:
        admin_panel()
    else:
        admin_login()

if __name__ == "__main__":
    main()
