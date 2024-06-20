import streamlit as st
from mysql.connector import Error
from db_operations import *

st.set_page_config(page_title="Subway Application Management", page_icon=":sandwich:", layout="wide")

def main():
    st.title("Subway Application Management")
    st.image("subway.png", width=200)
    
    choice = st.sidebar.radio("Navigation", ["Home", "Login", "Sign Up", "Admin Login"])

    if choice == "Home":
        st.subheader("Welcome to the Subway Application Management System")

    elif choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = get_user(email, password)
            if user:
                st.success(f"Welcome back! Your Employee Number is {user[0]}")
                user_profile(user[0])
            else:
                st.error("Invalid email or password")

    elif choice == "Sign Up":
        st.subheader("Create an Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        if password == confirm_password:
            if st.button("Sign Up"):
                emp_num = create_user(email, password)
                if emp_num:
                    st.success(f"Account created successfully! Your Employee Number is {emp_num}")
                    user_profile(emp_num)
                else:
                    st.error("Error creating account")
        else:
            st.error("Passwords do not match")

    elif choice == "Admin Login":
        st.subheader("Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type='password')
        if st.button("Login as Admin"):
            if admin_username == "admin1" and admin_password == "pass1":
                st.success("Logged in as Admin")
                admin_dashboard()
            else:
                st.error("Invalid admin credentials")

def user_profile(emp_num):
    st.subheader("User Profile")
    applicant_info = get_applicant_info(emp_num)
    
    if applicant_info:
        st.write(f"Employee Number: {emp_num}")
        st.write(f"Application Status: {applicant_info['application_status']}")
        
        with st.form("applicant_info_form"):
            st.subheader("I. APPLICANT INFORMATION")
            applicant_name = st.text_input("Name", applicant_info['applicant_name'])
            tax_ID_num = st.text_input("Tax ID Number", applicant_info['tax_ID_num'])
            applicant_address = st.text_input("Address", applicant_info['applicant_address'])
            applicant_tel_num = st.text_input("Telephone Number", applicant_info['applicant_tel_num'])
            age_verification = st.selectbox("Age Verification", ["Yes", "No"], index=["Yes", "No"].index(applicant_info['age_verification']))
            emergency_name = st.text_input("Emergency Contact Name", applicant_info['emergency_name'])
            emergency_tel_num = st.text_input("Emergency Contact Telephone", applicant_info['emergency_tel_num'])
            emergency_address = st.text_input("Emergency Contact Address", applicant_info['emergency_address'])
            position_type = st.selectbox("Position Type", ["Part time", "Full time", "Seasonal", "Temporary"], index=["Part time", "Full time", "Seasonal", "Temporary"].index(applicant_info['position_type']))
            total_hours = st.number_input("Total Hours Available", value=applicant_info['total_hours'])
            date_availability = st.date_input("Date of Availability", applicant_info['date_availability'])
            school_name = st.text_input("School Name", applicant_info['school_name'])
            school_address = st.text_input("School Address", applicant_info['school_address'])
            school_tel_num = st.text_input("School Telephone Number", applicant_info['school_tel_num'])
            counselor_name = st.text_input("Counselor Name", applicant_info['counselor_name'])
            grade_completed = st.text_input("Grade Completed", applicant_info['grade_completed'])
            GWA = st.number_input("GWA", value=applicant_info['GWA'], format="%.2f")
            graduated = st.selectbox("Graduated", ["Yes", "No"], index=["Yes", "No"].index(applicant_info['graduated']))
            enrolled = st.selectbox("Currently Enrolled", ["Yes", "No"], index=["Yes", "No"].index(applicant_info['enrolled']))

            st.subheader("II. EMPLOYMENT HISTORY")
            employment_history = get_employment_history(emp_num)
            for idx, history in enumerate(employment_history):
                with st.expander(f"Employment Record {idx+1}"):
                    company_name = st.text_input("Company Name", history['company_name'], key=f"company_name_{idx}")
                    company_address = st.text_input("Company Address", history['company_address'], key=f"company_address_{idx}")
                    company_tel_num = st.text_input("Company Telephone Number", history['company_tel_num'], key=f"company_tel_num_{idx}")
                    position = st.text_input("Position", history['position'], key=f"position_{idx}")
                    supervisor = st.text_input("Supervisor", history['supervisor'], key=f"supervisor_{idx}")
                    date_worked_from = st.date_input("Date Worked From", history['date_worked_from'], key=f"date_worked_from_{idx}")
                    date_worked_to = st.date_input("Date Worked To", history['date_worked_to'], key=f"date_worked_to_{idx}")
                    wage = st.text_input("Wage", history['wage'], key=f"wage_{idx}")
                    mgnt_ref_ck = st.text_input("Management Reference Check", history['mgnt_ref_ck'], key=f"mgnt_ref_ck_{idx}")
                    reason_for_leaving = st.text_input("Reason for Leaving", history['reason_for_leaving'], key=f"reason_for_leaving_{idx}")
                    permission = st.selectbox("Permission to Contact", ["Yes", "No"], index=["Yes", "No"].index(history['permission']), key=f"permission_{idx}")

            st.subheader("III. REFERENCES")
            references = get_references(emp_num)
            for idx, ref in enumerate(references):
                with st.expander(f"Reference {idx+1}"):
                    ref_name = st.text_input("Reference Name", ref['ref_name'], key=f"ref_name_{idx}")
                    ref_tel_num = st.text_input("Reference Telephone Number", ref['ref_tel_num'], key=f"ref_tel_num_{idx}")
                    years_known = st.number_input("Years Known", value=ref['years_known'], key=f"years_known_{idx}")
                    ref_address = st.text_input("Reference Address", ref['ref_address'], key=f"ref_address_{idx}")

            submitted = st.form_submit_button("Save")
            if submitted:
                applicant_data = (emp_num, applicant_name, tax_ID_num, applicant_address, applicant_tel_num, age_verification,
                        emergency_name, emergency_tel_num, emergency_address, position_type, total_hours,
                        date_availability, school_name, school_address, school_tel_num, counselor_name,
                        grade_completed, GWA, graduated, enrolled)
                update_applicant_info(applicant_data)

                for idx, history in enumerate(employment_history):
                    history_data = (
                        history['company_name'], history['company_address'], history['company_tel_num'], 
                        history['position'], history['supervisor'], history['date_worked_from'], 
                        history['date_worked_to'], history['wage'], history['mgnt_ref_ck'], 
                        history['reason_for_leaving'], history['permission']
                    )
                    update_employment_history(history['history_code'], history_data)

                for idx, ref in enumerate(references):
                    ref_data = (ref['ref_name'], ref['ref_tel_num'], ref['years_known'], ref['ref_address'])
                    update_reference(ref['ref_code'], ref_data)

                st.success("Information updated successfully")
    else:
        st.error("No applicant information found")

    if st.button("Logout"):
        st.experimental_rerun()

def admin_dashboard():
    st.subheader("Admin Dashboard")
    applicants = get_all_applicants()
    if applicants:
        for applicant in applicants:
            with st.expander(f"Applicant {applicant['emp_num']} - {applicant['applicant_name']}"):
                st.write(f"Application Status: {applicant['application_status']}")
                st.write(f"Name: {applicant['applicant_name']}")
                st.write(f"Address: {applicant['applicant_address']}")
                st.write(f"Telephone: {applicant['applicant_tel_num']}")
                st.write(f"Age Verification: {applicant['age_verification']}")
                st.write(f"Emergency Contact Name: {applicant['emergency_name']}")
                st.write(f"Emergency Contact Telephone: {applicant['emergency_tel_num']}")
                st.write(f"Emergency Contact Address: {applicant['emergency_address']}")
                st.write(f"Position Type: {applicant['position_type']}")
                st.write(f"Total Hours Available: {applicant['total_hours']}")
                st.write(f"Date of Availability: {applicant['date_availability']}")
                st.write(f"School Name: {applicant['school_name']}")
                st.write(f"School Address: {applicant['school_address']}")
                st.write(f"School Telephone: {applicant['school_tel_num']}")
                st.write(f"Counselor Name: {applicant['counselor_name']}")
                st.write(f"Grade Completed: {applicant['grade_completed']}")
                st.write(f"GWA: {applicant['GWA']}")
                st.write(f"Graduated: {applicant['graduated']}")
                st.write(f"Currently Enrolled: {applicant['enrolled']}")

                employment_history = get_employment_history(applicant['emp_num'])
                st.subheader("II. EMPLOYMENT HISTORY")
                for idx, history in enumerate(employment_history):
                    with st.expander(f"Employment Record {idx+1}"):
                        st.write(f"Company Name: {history['company_name']}")
                        st.write(f"Company Address: {history['company_address']}")
                        st.write(f"Company Telephone Number: {history['company_tel_num']}")
                        st.write(f"Position: {history['position']}")
                        st.write(f"Supervisor: {history['supervisor']}")
                        st.write(f"Date Worked From: {history['date_worked_from']}")
                        st.write(f"Date Worked To: {history['date_worked_to']}")
                        st.write(f"Wage: {history['wage']}")
                        st.write(f"Management Reference Check: {history['mgnt_ref_ck']}")
                        st.write(f"Reason for Leaving: {history['reason_for_leaving']}")
                        st.write(f"Permission to Contact: {history['permission']}")

                references = get_references(applicant['emp_num'])
                st.subheader("III. REFERENCES")
                for idx, ref in enumerate(references):
                    with st.expander(f"Reference {idx+1}"):
                        st.write(f"Reference Name: {ref['ref_name']}")
                        st.write(f"Reference Telephone Number: {ref['ref_tel_num']}")
                        st.write(f"Years Known: {ref['years_known']}")
                        st.write(f"Reference Address: {ref['ref_address']}")

                new_status = st.selectbox("Application Status", ["accepted", "not accepted"], index=["accepted", "not accepted"].index(applicant['application_status']))
                if st.button(f"Update Status for {applicant['emp_num']}"):
                    update_application_status(applicant['emp_num'], new_status)
                    st.success("Status updated successfully")

if __name__ == '__main__':
    main()
