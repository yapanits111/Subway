import streamlit as st
from db_operations import (
    create_user, 
    get_user, 
    get_user_by_email, 
    fetch_applicant_info, 
    add_applicant_info, 
    update_applicant_info, 
    fetch_employment_history, 
    add_employment_history, 
    fetch_references, 
    add_reference,
    fetch_all_applicants
)

def show_signup_page():
    st.title("Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if get_user(username):
            st.error("Username already taken")
        elif get_user_by_email(email):
            st.error("Email already registered")
        else:
            create_user(username, password, email)
            st.success("Account created successfully. Please login.")

def show_login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_data = fetch_applicant_info(username)
            st.success("Logged in successfully")
        else:
            st.error("Invalid username or password")

def show_admin_login_page():
    st.title("Admin Login")

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        admin_username = "admin"
        admin_password = "adminpass"
        
        if username == admin_username and password == admin_password:
            st.session_state.admin_logged_in = True
            st.success("Admin logged in successfully")
            show_admin_dashboard()
        else:
            st.error("Invalid admin credentials")

def show_admin_dashboard():
    st.title("Admin Dashboard")

    if st.button("View All Applicants"):
        applicants = fetch_all_applicants()
        for applicant in applicants:
            st.write(f"Applicant Name: {applicant['applicant_name']}")
            st.write(f"Tax ID: {applicant['tax_ID_num']}")
            st.write(f"Address: {applicant['applicant_address']}")
            st.write(f"Telephone: {applicant['applicant_tel_num']}")
            st.write(f"Position: {applicant['position_type']}")
            st.write("---")
            
            emp_history = fetch_employment_history(applicant["username"])
            if emp_history:
                st.write("Employment History:")
                for history in emp_history:
                    st.write(f"Company: {history['company_name']}, Position: {history['position']}, From: {history['date_worked_from']}, To: {history['date_worked_to']}")
                    st.write("---")
            
            references = fetch_references(applicant["username"])
            if references:
                st.write("References:")
                for ref in references:
                    st.write(f"Name: {ref['ref_name']}, Telephone: {ref['ref_tel_num']}, Years Known: {ref['years_known']}")
                    st.write("---")

def show_dashboard():
    st.title("Dashboard")

    if "user_data" in st.session_state:
        applicant_data = st.session_state.user_data
        st.write(f"Welcome {applicant_data['applicant_name']}")

        st.subheader("Applicant Info")
        st.write(applicant_data)

        st.subheader("Employment History")
        employment_history = fetch_employment_history(st.session_state.username)
        if employment_history:
            for history in employment_history:
                st.write(history)

        st.subheader("References")
        references = fetch_references(st.session_state.username)
        if references:
            for ref in references:
                st.write(ref)

        if st.button("Edit Info"):
            st.session_state.edit_mode = True

        if st.session_state.get("edit_mode"):
            st.subheader("Edit Applicant Info")

            applicant_data["applicant_name"] = st.text_input("Applicant Name", value=applicant_data["applicant_name"])
            applicant_data["tax_ID_num"] = st.text_input("Tax ID Number", value=applicant_data["tax_ID_num"])
            applicant_data["applicant_address"] = st.text_input("Applicant Address", value=applicant_data["applicant_address"])
            applicant_data["applicant_tel_num"] = st.text_input("Applicant Telephone Number", value=applicant_data["applicant_tel_num"])
            applicant_data["age_verification"] = st.selectbox("Age Verification", ["Yes", "No"], index=["Yes", "No"].index(applicant_data["age_verification"]))
            applicant_data["emergency_name"] = st.text_input("Emergency Contact Name", value=applicant_data["emergency_name"])
            applicant_data["emergency_tel_num"] = st.text_input("Emergency Contact Telephone Number", value=applicant_data["emergency_tel_num"])
            applicant_data["emergency_address"] = st.text_input("Emergency Contact Address", value=applicant_data["emergency_address"])
            applicant_data["position_type"] = st.selectbox("Position Type", ["Part time", "Full time", "Seasonal", "Temporary"], index=["Part time", "Full time", "Seasonal", "Temporary"].index(applicant_data["position_type"]))
            applicant_data["total_hours"] = st.number_input("Total Hours Available", value=applicant_data["total_hours"])
            applicant_data["date_availability"] = st.date_input("Date of Availability", value=applicant_data["date_availability"])
            applicant_data["school_name"] = st.text_input("School Name", value=applicant_data["school_name"])
            applicant_data["school_address"] = st.text_input("School Address", value=applicant_data["school_address"])
            applicant_data["school_tel_num"] = st.text_input("School Telephone Number", value=applicant_data["school_tel_num"])
            applicant_data["counselor_name"] = st.text_input("Counselor Name", value=applicant_data["counselor_name"])
            applicant_data["grade_completed"] = st.text_input("Grade Completed", value=applicant_data["grade_completed"])
            applicant_data["GWA"] = st.number_input("GWA", value=applicant_data["GWA"])
            applicant_data["graduated"] = st.selectbox("Graduated", ["Yes", "No"], index=["Yes", "No"].index(applicant_data["graduated"]))
            applicant_data["enrolled"] = st.selectbox("Enrolled", ["Yes", "No"], index=["Yes", "No"].index(applicant_data["enrolled"]))

            if st.button("Save"):
                update_applicant_info(applicant_data)
                st.success("Information updated successfully")
                st.session_state.edit_mode = False

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Sign Up", "Admin Login"])

    if page == "Login":
        show_login_page()
        if st.session_state.get("logged_in"):
            show_dashboard()
    elif page == "Sign Up":
        show_signup_page()
    elif page == "Admin Login":
        show_admin_login_page()

if __name__ == "__main__":
    main()
