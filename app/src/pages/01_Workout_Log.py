import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import datetime
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Arnold\'s Workout Logger')

GET_API_URL = f"http://web-api:4000/c/workout_log/33"
POST_API_URL = "http://web-api:4000/c/workout_log"

# Create tabs for viewing and adding workout logs
tab1, tab2 = st.tabs(["View Workout Logs", "Add New Workout"])

with tab1:
    try:
        # Log the URL we're trying to connect to
        logger.info(f"Connecting to API at: {GET_API_URL}")
        
        with st.spinner("Loading workout logs..."):
            # Send GET request to Flask backend
            response = requests.get(GET_API_URL, timeout=5)
            
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
                st.info(f"Attempted to connect to: {GET_API_URL}")
                
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info(f"Attempted to connect to: {GET_API_URL}")

with tab2:
    st.subheader("Add New Workout Entry")
    
    # Create form for new workout entry
    with st.form("workout_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Get today's date as default
            default_date = datetime.datetime.now().strftime("%Y-%m-%d")
            workout_date = st.date_input("Workout Date", value=pd.to_datetime(default_date))
            
            # Convert the date to string format for the API
            formatted_date = workout_date.strftime("%Y-%m-%d")
            
            workout_type = st.selectbox(
                "Workout Type", 
                ["Strength Training", "Cardio", "Flexibility", "HIIT", "Crossfit", "Other"]
            )
            
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=60)
            
            intensity = st.select_slider(
                "Workout Intensity",
                options=["Very Light", "Light", "Moderate", "Vigorous", "Maximum"],
                value="Moderate"
            )
        
        with col2:
            exercise_name = st.text_input("Exercise Name", "")
            
            sets = st.number_input("Number of Sets", min_value=1, max_value=20, value=3)
            
            reps = st.number_input("Number of Reps", min_value=1, max_value=100, value=10)
            
            weight = st.number_input("Weight (if applicable, in kg)", min_value=0, max_value=500, value=0)
        
        notes = st.text_area("Notes (optional)", "")
        
        # Submit button
        submitted = st.form_submit_button("Log Workout")
        
        if submitted:
            # Prepare data for API
            workout_data = {
                "client_id": 33,
                "date": formatted_date,
                "workout_type": workout_type,
                "duration": int(duration),
                "intensity": intensity,
                "exercise_name": exercise_name,
                "sets": int(sets),
                "reps": int(reps),
                "weight": float(weight),
                "notes": notes
            }
            
            try:
                # Send POST request to API
                logger.info(f"Posting workout data to: {POST_API_URL}")
                response = requests.post(POST_API_URL, json=workout_data, timeout=5)
                
                if response.status_code == 201:
                    st.success("Workout successfully logged!")
                    # Refresh the page to show the updated list
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to log workout. Status code: {response.status_code}")
                    if response.text:
                        st.error(f"Error details: {response.text}")
            
            except Exception as e:
                st.error(f"Error submitting workout data: {str(e)}")

    # Add some helpful information
    with st.expander("Workout Logging Tips"):
        st.markdown("""
        ### Tips for effective workout logging:
        
        - Be specific with exercise names (e.g., "Barbell Bench Press" instead of just "Bench Press")
        - For cardio workouts, use the notes section to record distance or specific intervals
        - Record your perceived exertion for better tracking over time
        - Include any modifications or variations in the notes section
        """)