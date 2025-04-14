import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Workout Logger')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# Button to fetch workout logs
if st.button("Fetch Workout Logs"):
    url = "http://web-api:4000/workout_log/33"
    
    # Send GET request to your Flask backend
    response = requests.get(url)

    # Handle valid response
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            df = pd.DataFrame(data)
            st.subheader("Workout Logs for Client ID 33")
            st.dataframe(df)
        else:
            st.warning("No workout logs found for this client.")
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
