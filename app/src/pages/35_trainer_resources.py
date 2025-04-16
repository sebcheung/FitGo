import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://web-api:4000/t"

st.set_page_config(layout="wide")

# Button to navigate back to trainer dashboard
col1, col2, col3 = st.columns([8, 1, 1])
with col3:
    if st.button("⬅️ Back"):
        st.switch_page('pages/31_trainer_home.py') 

st.title("🏥 Health Metrics & 📚 Trainer Resources")

trainer_id = st.session_state.get("user_id", 1)

st.header("💓 Client Health Metrics")

# Health metrics section
with st.form("get_health_metrics"):
    # Get client id
    client_id = st.text_input("Client ID to view health data", "1")
    if st.form_submit_button("Retrieve Health Metrics"):
        # Retrieve health metrics through API
        resp = requests.get(f"{BASE_URL}/health_metrics/{client_id}")
        if resp.ok:
            data = resp.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("No health metrics found.")
        else:
            st.error("Failed to fetch health data.")

st.subheader("➕ Add New Health Metric")
with st.form("add_health"):
    # Info needed to add a new health metric
    user_id = st.text_input("Client ID", "")
    heart_rate = st.number_input("Heart Rate", value=70)
    calories = st.number_input("Calories Burned", value=200)
    sleep = st.number_input("Sleep Duration (hrs)", value=8.0)
    blood = st.text_input("Blood Pressure Level", "120/80")
    water = st.number_input("Water Intake (L)", value=2.0)
    calories_in = st.number_input("Caloric Intake", value=2200)
    fat = st.number_input("Body Fat (%)", value=20.0)
    if st.form_submit_button("Add Metric"):
        payload = {
            "user_id": user_id,
            "heart_rate": heart_rate,
            "calories_burned": calories,
            "sleep_duration": sleep,
            "blood_pressure_level": blood,
            "water_intake": water,
            "caloric_intake": calories_in,
            "body_fat_percentage": fat
        }
        # Use API to add the health metric
        r = requests.post(f"{BASE_URL}/health_metrics", json=payload)
        st.success("Metric added!" if r.ok else "Failed to add metric.")

st.subheader("✏️ Update Existing Metric")
with st.form("update_health"):
    # Info needed to update a metric
    record_id = st.text_input("Record ID to update")
    new_heart_rate = st.number_input("New Heart Rate", value=75)
    new_calories = st.number_input("New Calories Burned", value=250)
    new_sleep = st.number_input("New Sleep Duration (hrs)", value=7.5)
    new_bp = st.text_input("New Blood Pressure", "110/70")
    new_water = st.number_input("New Water Intake", value=2.5)
    new_calories_in = st.number_input("New Caloric Intake", value=2100)
    new_fat = st.number_input("New Body Fat %", value=18.0)
    if st.form_submit_button("Update Metric"):
        update_data = {
            "heart_rate": new_heart_rate,
            "calories_burned": new_calories,
            "sleep_duration": new_sleep,
            "blood_pressure_level": new_bp,
            "water_intake": new_water,
            "caloric_intake": new_calories_in,
            "body_fat_percentage": new_fat
        }
        # Update health metric through API
        r = requests.put(f"{BASE_URL}/health_metrics/{record_id}", json=update_data)
        st.success("Metric updated!" if r.ok else "Update failed.")

st.header("📚 Trainer Resources")

# View resources through API
resp = requests.get(f"{BASE_URL}/resources")
if resp.ok:
    resources = pd.DataFrame(resp.json())
    if not resources.empty:
        st.dataframe(resources)
    else:
        st.info("No resources available.")
else:
    st.error("Failed to fetch resources.")

st.subheader("➕ Add New Resource")
with st.form("add_resource"):
    # Info needed to add a new resource
    res_title = st.text_input("Title")
    res_url = st.text_input("URL")
    res_type = st.selectbox("Type", ["Video", "PDF", "Article", "Tool"])
    if st.form_submit_button("Add Resource"):
        payload = {
            "Title": res_title,
            "URL": res_url,
            "Type": res_type,
            "Trainer_ID": trainer_id
        }
        # Use API to add a resource
        r = requests.post(f"{BASE_URL}/resources", json=payload)
        st.success("Resource added!" if r.ok else "Failed to add resource.")
