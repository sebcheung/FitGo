import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Arnold\'s Workout Logger')

# API URLs
API_URL = f"http://web-api:4000/c/workout_log/33"

# Create tabs for viewing and adding workout logs
tab1, tab2 = st.tabs(["View Workout Logs", "Add New Workout"])

with tab1:
    try:
        # Log the URL we're trying to connect to
        logger.info(f"Connecting to API at: {API_URL}")
        
        with st.spinner("Loading workout logs..."):
            # Send GET request to Flask backend
            response = requests.get(API_URL, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    df = pd.DataFrame(data)
                    st.subheader(f"Workout Logs for {st.session_state.get('first_name', 'User')}")
                    st.dataframe(df)
                else:
                    st.warning("No workout logs found for this client.")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                st.info(f"Attempted to connect to: {API_URL}")
                
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info(f"Attempted to connect to: {API_URL}")

with tab2:
    st.subheader("Add New Workout Entry")
    
    # Create form for new workout entry
    with st.form("workout_form", clear_on_submit=True):
        # Use the same field names as in your Flask route
        total_weight = st.number_input("Total Weight (kg)", min_value=0, max_value=1000, value=100)
        total_time = st.number_input("Total Time (minutes)", min_value=1, max_value=300, value=60)
        
        # Submit button
        submitted = st.form_submit_button("Log Workout")
        
        if submitted:
            # Prepare data for API - match the field names in your Flask backend
            workout_data = {
                "Total_Weight": int(total_weight),
                "Total_Time": int(total_time)
            }
            
            try:
                # Send POST request to API - use the same URL as GET
                logger.info(f"Posting workout data to: {API_URL}")
                response = requests.post(API_URL, json=workout_data, timeout=5)
                
                if response.status_code == 201:
                    st.success("Workout successfully logged!")
                    # Refresh the page to show the updated list
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to log workout. Status code: {response.status_code}")
                    if hasattr(response, 'text'):
                        st.error(f"Error details: {response.text}")
            
            except Exception as e:
                st.error(f"Error submitting workout data: {str(e)}")

    # Add some helpful information
    with st.expander("Workout Logging Tips"):
        st.markdown("""
        ### Tips for effective workout logging:
        
        - **Total Weight**: This is the cumulative weight lifted across all exercises
        - **Total Time**: The total duration of your workout in minutes
        - Log your workouts consistently for better progress tracking
        - Consider adding more details to your workout routine over time
        """)