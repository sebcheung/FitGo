import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.write('# Manage Equipment')

# Display equipment for a gym
st.write('## Equipment List')

with st.form('Get Gym ID'):
    gym_id = st.text_input('Gym ID:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        list = requests.get(f'http://api:4000/go/equipments/{gym_id}').json()

        try:
            list_df = pd.DataFrame(list)
            cols = ['Equipment_ID', 'Name', 'Brand', 'Type', 'Purchase_Date', 'Status']
            list_df = list_df[cols]
            st.dataframe(list_df)
        except:
            st.write('Could not connect to database to get equipment list!')


# Create form to create a new piece of equipment
st.write('## Add Equipment')

with st.form('Add a New Piece of Equipment'):
    gym_id = st.text_input('Gym ID:')
    brand = st.text_input('Brand:')
    name = st.text_input('Equipment Name:')
    type = st.text_input('Type:')
    status = st.text_input('Status')
    purchase_date = st.date_input('Purchase Date:')

    purchase_date = purchase_date.strftime('%Y-%m-%d')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['Gym_ID'] = gym_id
        data['Type'] = type
        data['Purchase_Date'] = purchase_date
        data['Name'] = name
        data['Status'] = status
        data['Brand'] = brand

        response = requests.post('http://api:4000/go/equipments', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to add new equipment!')
        
# Create form to update a piece of equipment
st.write('## Update Equipment Status')

with st.form('Update Equipment Status'):
    gym_id = st.text_input('Gym ID:')
    equip_id = st.text_input('Equipment ID:')
    status = st.text_input('Updated Status:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['Gym_ID'] = gym_id
        data['Equipment_ID'] = equip_id
        data['Status'] = status

        response = requests.put('http://api:4000/go/equipments', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to update equipment {equip_id}')










