import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.write('# Manage Events')

# Display event attendees
st.write('## Event Attendees List')
 
list = requests.get('http://api:4000/go/events').json()
 
try:
    list_df = pd.DataFrame(list)
    cols = ['Event_ID', 'Event_Name', 'Host_Name', 'Event_Date', 'Attendees']
    list_df = list_df[cols]
    st.dataframe(list_df)
except:
    st.write('Could not connect to database to get attendees list!')

# Create form to create a new event
st.write('## Create Event')

with st.form('Create a New Event'):
    event_name = st.text_input('Event Name:')
    host_name = st.text_input('Host Name:')
    sponsor = st.text_input('Sponsor:')
    location = st.text_input('Location:')
    event_date = st.date_input('Event Date:')
    start_time = st.time_input('Start Time:')
    description = st.text_input('Description')

    event_date = event_date.strftime('%Y-%m-%d')
    start_time = start_time.strftime('%H:%M:%S')
    full_start_time = f'{event_date} {start_time}'

    submitted = st.form_submit_button('Submit')

    if submitted:
        data = {}
        data['Event_Name'] = event_name
        data['Host_Name'] = host_name
        data['Sponsor'] = sponsor
        data['Event_Location'] = location
        data['Event_Date'] = event_date
        data['Start_Time'] = full_start_time
        data['Event_Description'] = description

        response = requests.post('http://api:4000/go/events', json = data)

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to add new event!')
        
# Create form to cancel an event
st.write('## Cancel Event')

with st.form('Cancel an Existing Event'):
    event_id = st.text_input('Event ID:')

    submitted = st.form_submit_button('Submit')

    if submitted:
        response = requests.delete(f'http://api:4000/go/events/{event_id}')

        if response.status_code == 200:
            st.success(response.text)
        else:
            st.error(f'Failed to delete event {event_id}')










