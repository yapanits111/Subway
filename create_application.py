import streamlit as st
from db_functions import create_applicant_info, create_employment_history, create_reference, get_last_inserted_id
from datetime import date

if 'employment_history' not in st.session_state:
    st.session_state.employment_history = [{
        'company_name': "",
        'company_address': "",
        'company_tel_num': "",
        'position': "",
        'supervisor': "",
        'date_worked_from': date.today(),
        'date_worked_to': date.today(),
        'wage': "",
        'mgnt_ref_ck': "",
        'reason_for_leaving': "",
        'permission': "Yes"
    }]

if 'reference' not in st.session_state:
    st.session_state.reference = [{
        'ref_name': "",
        'ref_tel_num': "",
        'years_known': 0,
        'ref_address': ""
    }]

def add_employment_history():
    st.session_state.employment_history.append({
        'company_name': "",
        'company_address': "",
        'company_tel_num': "",
        'position': "",
        'supervisor': "",
        'date_worked_from': date.today(),
        'date_worked_to': date.today(),
        'wage': "",
        'mgnt_ref_ck': "",
        'reason_for_leaving': "",
        'permission': "Yes"
    })

def add_reference():
    st.session_state.reference.append({
        'ref_name': "",
        'ref_tel_num': "",
        'years_known': 0,
        'ref_address': ""
    })

def new_application():
    st.header("Employment Application Form")
    st.divider()
    st.subheader("*I. Personal Information*")
    applicant_name = st.text_input("Full Name")
    tax_ID_num = st.text_input("Tax ID Number")
    applicant_address = st.text_input("Address")
    applicant_tel_num = st.text_input("Cell/Telephone Number")
    age_verification = st.radio("Are You 16 years of age or over?", ["Yes", "No"], index=0)
    st.divider()

    st.subheader("*II. In Case of Emergency, Notify*")
    emergency_name = st.text_input("Emergency Contact Name")
    emergency_tel_num = st.text_input("Contact Number")
    emergency_address = st.text_input("Contact Address")
    st.divider()

    st.subheader("*III. Availability*")
    position_type = st.radio("Position Type", ["Part Time", "Full Time", "Seasonal", "Temporary"], index=0)
    total_hours = st.number_input("Total Hours Available Per Week", min_value=0)
    date_availability = st.date_input("Date Available to Start Work")
    st.divider()

    st.subheader("*IV. School Most Recent Attended*")
    school_name = st.text_input("School Name")
    school_address = st.text_input("School Address")
    school_tel_num = st.text_input("School Telephone Number")
    counselor_name = st.text_input("Counselor Name")
    grade_completed = st.radio("Last Grade Completed", ['Elementary', 'Junior High School', 'Senior High School', 'College'], index=0, horizontal =True)
    GWA = st.number_input("Most Recent GWA")
    graduated = st.radio("Graduated?", ["Yes", "No"], index=0)
    enrolled = st.radio("Now Enrolled?", ["Yes", "No"], index=0)
    st.divider()

    st.subheader("*V. Most Recent Employment*")
    for i, emp in enumerate(st.session_state.employment_history):
        st.write(f"Employment History {i+1}")
        emp['company_name'] = st.text_input(f"Company Name", value=emp['company_name'], key=f'company_name_{i+1}')
        emp['company_address'] = st.text_input(f"Company Address", value=emp['company_address'], key=f'company_address_{i+1}')
        emp['company_tel_num'] = st.text_input(f"Company Telephone Number", value=emp['company_tel_num'], key=f'company_tel_num_{i+1}')
        emp['position'] = st.text_input(f"Position", value=emp['position'], key=f'position_{i+1}')
        emp['supervisor'] = st.text_input(f"Supervisor", value=emp['supervisor'], key=f'supervisor_{i+1}')
        emp['date_worked_from'] = st.date_input(f"Date Worked From", value=emp['date_worked_from'], key=f'date_worked_from_{i+1}')
        emp['date_worked_to'] = st.date_input(f"Date Worked To", value=emp['date_worked_to'], key=f'date_worked_to_{i+1}')
        emp['wage'] = st.text_input(f"Wage", value=emp['wage'], key=f'wage_{i+1}')
        emp['mgnt_ref_ck'] = st.text_input(f"Management Reference Checked By", value=emp['mgnt_ref_ck'], key=f'mgnt_ref_ck_{i+1}')
        emp['reason_for_leaving'] = st.text_input(f"Reason for Leaving", value=emp['reason_for_leaving'], key=f'reason_for_leaving_{i+1}')
        emp['permission'] = st.radio(f"Do we have your permission to contact your previous employer?", ['Yes', 'No'], index=0 if emp['permission'] == "Yes" else 1, key=f'permission_{i+1}')

    if st.button("Add Employment History"):
        add_employment_history()

    st.subheader("*VI. References*")
    for j, ref in enumerate(st.session_state.reference):
        st.write(f"Reference Person {j+1}")
        ref['ref_name'] = st.text_input(f"Full Name", value=ref['ref_name'], key=f'ref_name_{j+1}')
        ref['ref_tel_num'] = st.text_input(f"Tel. Number", value=ref['ref_tel_num'], key=f'ref_tel_num_{j+1}')
        ref['years_known'] = st.number_input(f"Years Known", value=ref['years_known'], min_value=0, key=f'years_known_{j+1}')
        ref['ref_address'] = st.text_input(f"Home Address", value=ref['ref_address'], key=f'ref_address_{j+1}')

    if st.button("Add Reference"):
        add_reference()

    if st.button("Create Application"):
        try:
            empInfo = (
                applicant_name, tax_ID_num, applicant_address, applicant_tel_num, age_verification,
                emergency_name, emergency_tel_num, emergency_address, position_type, total_hours,
                date_availability.strftime('%Y-%m-%d'), school_name, school_address, school_tel_num, counselor_name,
                grade_completed, GWA, graduated, enrolled
            )
            create_applicant_info(empInfo)
            emp_num = get_last_inserted_id()
            if emp_num is None:
                st.error("Failed to get the last inserted employee number.")
                return

            for empHist in st.session_state.employment_history:
                employment_history = (
                    emp_num, empHist['company_name'], empHist['company_address'], empHist['company_tel_num'],
                    empHist['position'], empHist['supervisor'],
                    empHist['date_worked_from'].strftime('%Y-%m-%d'), empHist['date_worked_to'].strftime('%Y-%m-%d'),
                    empHist['wage'], empHist['mgnt_ref_ck'], empHist['reason_for_leaving'],
                    empHist['permission']
                )
                create_employment_history(employment_history)
                emp_num = get_last_inserted_id()
                if emp_num is None:
                    return
                history_code = get_last_inserted_id()
                if history_code is None:
                    return

            for empRef in st.session_state.reference:
                reference = (
                    emp_num, empRef['ref_name'], empRef['ref_tel_num'], empRef['years_known'], empRef['ref_address']
                )
                create_reference(reference)
                emp_num = get_last_inserted_id()
                if emp_num is None:
                    return    
                ref_code = get_last_inserted_id()
                if ref_code is None:
                    return

            st.success("Application Created Successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    new_application()
