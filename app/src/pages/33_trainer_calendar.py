import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta

# Change 'web-api' to 'localhost' if running outside Docker
BASE_URL = "http://web-api:4000/t"

# Get trainer ID from session
trainer_id = st.session_state.get("user_id", "1")
st.header("📅 Training Calendar")

# Retrieve sessions for the trainer
st.subheader("📥 Scheduled Sessions")

response = requests.get(f"{BASE_URL}/training_session/{trainer_id}")

if response.ok:
    sessions = response.json()

    if sessions:
        df = pd.DataFrame(sessions)
        df["Date_time"] = pd.to_datetime(df["Date_time"])
        df["End_time"] = df["Date_time"] + timedelta(hours=1)

        # Calendar View
        st.subheader("📊 Calendar View")
        calendar = px.timeline(
            df,
            x_start="Date_time",
            x_end="End_time",
            y="Client_ID",
            color="Status",
            hover_data=["Class_description", "Session_ID"],
            title="Trainer Schedule"
        )
        calendar.update_yaxes(categoryorder="total ascending")
        calendar.update_layout(height=500, margin={"t": 50, "b": 20})
        st.plotly_chart(calendar, use_container_width=True)

        # Data Table
        st.subheader("📋 Upcoming Sessions")
        st.dataframe(df[["Session_ID", "Client_ID", "Date_time", "Status", "Class_description"]])
    else:
        st.info("No sessions scheduled.")
else:
    st.error("Failed to fetch training sessions.")

# Add a new training session
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

# Cancel a training session
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
