import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.write('# Manage Employee Roster')

st.write('## Add Employee')

with st.form('Add a New Employee'):
    first = st.text_input('First Name:')
    last = st.text_input('Last Name:')
    age = st.text_input('Age:')
    ssn = st.text_input('Social Security Number:')
    address = st.text_input('Address:')
    boss_id = st.text_input('Boss ID:')
    hire_date = st.date_input('Hire Date:')

    hire_date = hire_date.strftime('%Y-%m-%d')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['FirstName'] = first
        data['LastName'] = last
        data['Age'] = age
        data['SSN'] = ssn
        data['Address'] = address
        data['Boss_ID'] = boss_id
        data['Hire_Date'] = hire_date

        response = requests.post('http://api:4000/go/employees', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to add new employee!')
        

st.write('## Update Employee')

with st.form('Update Information for an Existing Employee'):
    emp_id = st.text_input('Employee ID:')
    first = st.text_input('New First Name:')
    last = st.text_input('New Last Name:')
    age = st.text_input('New Age:')
    address = st.text_input('New Address:')
    boss_id = st.text_input('New Boss ID:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['Employee_ID'] = emp_id
        data['FirstName'] = first
        data['LastName'] = last
        data['Age'] = age
        data['Address'] = address
        data['Boss_ID'] = boss_id

        response = requests.put('http://api:4000/go/employees', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to update employee {emp_id}')

st.write('## Delete Employee')

with st.form('Delete an Existing Employee'):
    emp_id = st.text_input('Employee ID:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        response = requests.delete(f'http://api:4000/go/employees/{emp_id}')

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to delete employee {emp_id}')










