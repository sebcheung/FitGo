import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.write('# Manage Client Roster')

# Display client roster
st.write('## Client Roster')
 
roster = requests.get('http://api:4000/go/clients').json()
 
try:
    roster_df = pd.DataFrame(roster)
    cols = ['Client_ID', 'FirstName', 'LastName', 'Join_Date', 'Sex', 'Age', 'Weight', 'Height', 'Email', 'Phone_Number']
    roster_df = roster_df[cols]
    st.dataframe(roster_df)
except:
    st.write('Could not connect to database to get client roster!')

# Create form to add new client
st.write('## Add Client')

with st.form('Add a New Client'):
    first = st.text_input('First Name:')
    last = st.text_input('Last Name:')
    age = st.text_input('Age:')
    sex = st.text_input('Sex:')
    weight = st.text_input('Weight:')
    height = st.text_input('Height:')
    email = st.text_input('Email:')
    phone = st.text_input('Phone Number:')
    join_date = st.date_input('Join Date:')

    join_date = join_date.strftime('%Y-%m-%d')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['FirstName'] = first
        data['LastName'] = last
        data['Age'] = age
        data['Sex'] = sex
        data['Weight'] = weight
        data['Height'] = height
        data['Email'] = email
        data['Phone'] = phone
        data['Join_Date'] = join_date

        response = requests.post('http://api:4000/go/clients', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to add new client!')
        
# Create form to update an existing client
st.write('## Update Client')

with st.form('Update Information for an Existing Client'):
    client_id = st.text_input('Client ID:')
    first = st.text_input('Updated First Name:')
    last = st.text_input('Updated Last Name:')
    age = st.text_input('Updated Age:')
    email = st.text_input('Updated Email:')
    phone = st.text_input('Updated Phone Number:')
    sex = st.text_input('Updated Sex:')
    weight = st.text_input('Updated Weight:')
    height = st.text_input('Updated Height:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['Client_ID'] = client_id
        data['FirstName'] = first
        data['LastName'] = last
        data['Age'] = age
        data['Sex'] = sex
        data['Weight'] = weight
        data['Height'] = height
        data['Email'] = email
        data['Phone_Number'] = phone

        response = requests.put('http://api:4000/go/clients', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to update client {client_id}')

# Create form to delete an existing client
st.write('## Delete Client')

with st.form('Delete an Existing Client'):
    client_id = st.text_input('Client ID:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        response = requests.delete(f'http://api:4000/go/clients/{client_id}')

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to delete employee {client_id}')










