import streamlit as st
import pandas as pd
import requests
from datetime import timedelta

# Change localhost if running outside Docker
BASE_URL = "http://web-api:4000/t"

# Button to navigate back to trainer dashboard
col1, col2, col3 = st.columns([8, 1, 1])
with col3:
    if st.button("⬅️ Back"):
        st.switch_page('pages/31_trainer_home.py') 

# Get trainer ID from session
trainer_id = st.session_state.get("user_id", "1")
st.header("📅 Training Calendar")

# Retrieve currently scheduled training sessions through the API
response = requests.get(f"{BASE_URL}/training_session/{trainer_id}")

if response.ok:
    sessions = response.json()

    if sessions:
        df = pd.DataFrame(sessions)
        df["Date_time"] = pd.to_datetime(df["Date_time"])
        df["End_time"] = df["Date_time"] + timedelta(hours=1)

        # Data Table
        st.subheader("📋 Upcoming Sessions")
        st.dataframe(df[["Session_ID", "Client_ID", "Date_time", "Status", "Class_description"]])
    else:
        st.info("No sessions scheduled.")
else:
    st.error("Failed to fetch training sessions.")

st.subheader("➕ Create New Session")

with st.form("new_session"):
    # Info needed to enter for a new session
    client_id = st.text_input("Client ID")
    date = st.date_input("Date")
    time = st.time_input("Time")
    description = st.text_input("Class Description")
    status = st.selectbox("Status", ["Scheduled", "Pending", "Confirmed"])
    max_participants = st.number_input("Max Participants", 1, 50, 15)

    if st.form_submit_button("Create Session"):
        datetime_str = f"{date} {time}"
        session_data = {
            "trainer_id": trainer_id,
            "status": status,
            "date_time": datetime_str,
            "class_description": description,
            "max_participants": max_participants
        }

        # Add training session through API
        create_resp = requests.post(f"{BASE_URL}/training_session/{client_id}", json=session_data)

        if create_resp.ok:
            st.success("Session created!")
            st.rerun()
        else:
            st.error("Failed to create session.")

st.subheader("❌ Cancel Session")

with st.form("cancel_session"):
    # Specify client and session id to cancel
    cancel_client_id = st.text_input("Client ID for cancellation")
    cancel_session_id = st.text_input("Session ID to cancel")

    if st.form_submit_button("Cancel Session"):
        # Delete a training session through API
        delete_resp = requests.delete(f"{BASE_URL}/training_session/{cancel_client_id}/{cancel_session_id}")
        if delete_resp.ok:
            st.success("Session cancelled.")
            st.rerun()
        else:
            st.error("Failed to cancel session.")
