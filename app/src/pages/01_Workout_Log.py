import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Arnold\'s Workout Logger')

api_url = "http://web-api:4000/c/workout_log/33"

try:
    # Log the URL we're trying to connect to
    logger.info(f"Connecting to API at: {api_url}")
    
    with st.spinner("Loading workout logs..."):
        # Send GET request to Flask backend
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                df = pd.DataFrame(data)
                st.subheader(f"Workout Logs {st.session_state['first_name']}")
                st.dataframe(df)
            else:
                st.warning("No workout logs found for this client.")
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            st.info(f"Attempted to connect to: {api_url}")
            
except Exception as e:
    st.error(f"Connection error: {str(e)}")
    st.info(f"Attempted to connect to: {api_url}")
