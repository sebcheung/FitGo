import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("🏥 Health Metrics & 📚 Trainer Resources")

if 'user_id' in st.session_state:
    trainer_id = st.session_state.get("user_id", 1)
else:
    trainer_id = 1

BASE_URL = "http://web-api:4000/t"

tab1, tab2 = st.tabs(["Health Metrics", "Trainer Resources"])

with tab1:
    st.header("💓 Client Health Metrics")

    with st.form("get_health_metrics"):
        # Get client id
        client_id = st.text_input("Client ID to view health data", "33")
        submitted = st.form_submit_button("Retrieve Health Metrics")
        
        if submitted:
            # Get health metrics through API
            try:
                resp = requests.get(f"{BASE_URL}/health_metrics/{client_id}")
                if resp.ok:
                    data = resp.json()
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                        
                    else:
                        st.info("No health metrics found.")
                else:
                    st.error(f"Failed to fetch health data.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Add New Health Metric")
        with st.form("add_health"):
            # Info needed to add a new health metric
            user_id = st.text_input("Client ID", "33")
            heart_rate = st.number_input("Heart Rate", value=70)
            calories = st.number_input("Calories Burned", value=200)
            sleep = st.number_input("Sleep Duration (hrs)", value=8)
            blood = st.selectbox("Blood Pressure Level", ["Normal", "Elevated"])
            water = st.number_input("Water Intake (L)", value=2.0)
            calories_in = st.number_input("Caloric Intake", value=2200)
            fat = st.number_input("Body Fat (%)", value=20.0)
            
            if st.form_submit_button("Add Metric"):
                payload = {
                    "User_ID": int(user_id),
                    "Heart_Rate": int(heart_rate),
                    "Calories_Burned": int(calories),
                    "Sleep_Duration": int(sleep),
                    "Blood_Pressure_Level": blood,
                    "Water_Intake": float(water),
                    "Caloric_Intake": int(calories_in),
                    "Body_Fat_Percentage": float(fat)
                }
                
                # Use API to add the health metric
                try:
                    health_url = f"{BASE_URL}/health_metrics/{user_id}"
                    
                    r = requests.post(health_url, json=payload)
                    if r.status_code == 201:
                        st.success("Metric added successfully!")
                    else:
                        st.error(f"Failed to add metric.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col2:
        st.subheader("✏️ Update Existing Metric")
        
        # Get available records
        client_for_update = st.text_input("Client ID for update", "33")
        
        if st.button("Fetch Records"):
            try:
                resp = requests.get(f"{BASE_URL}/health_metrics/{client_for_update}")
                if resp.ok and resp.json():
                    records = pd.DataFrame(resp.json())
                    record_options = [f"{r['Record_ID']}: {r.get('Date', 'No date')}" for _, r in records.iterrows()]
                    
                    if 'record_options' not in st.session_state:
                        st.session_state.record_options = record_options
                        st.session_state.records = records.to_dict('records')
                    
                    st.success(f"Found {len(record_options)} records")
                else:
                    st.warning("No records found for this client")
            except Exception as e:
                st.error(f"Error fetching records: {str(e)}")
        
        with st.form("update_health"):
            if 'record_options' in st.session_state and st.session_state.record_options:
                selected_record = st.selectbox("Select Record", st.session_state.record_options)
                record_id = selected_record.split(":")[0] if selected_record else ""
                
                # Basic fields to update
                new_heart_rate = st.number_input("New Heart Rate", value=75)
                new_calories = st.number_input("New Calories Burned", value=250)
            else:
                record_id = st.text_input("Record ID to update")
                new_heart_rate = st.number_input("New Heart Rate", value=75)
                new_calories = st.number_input("New Calories Burned", value=250)
            
            if st.form_submit_button("Update Metric"):
                if record_id:
                    update_data = {
                        "Heart_Rate": int(new_heart_rate),
                        "Calories_Burned": int(new_calories)
                    }
                    
                    # Update health metric through API
                    try:
                        update_url = f"{BASE_URL}/health_metrics/{client_for_update}/{record_id}"
                        
                        r = requests.put(update_url, json=update_data)
                        if r.status_code == 200:
                            st.success("Metric updated successfully!")
                        else:
                            st.error(f"Update failed.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please select or enter a record ID")

with tab2:
    st.header("📚 Trainer Resources")

    # View resources through API
    try:
        resp = requests.get(f"{BASE_URL}/resources")
        if resp.ok:
            if resp.json():
                resources = pd.DataFrame(resp.json())
                st.dataframe(resources, use_container_width=True)
            else:
                st.info("No resources available.")
        else:
            st.warning(f"Failed to fetch resources.")
    except Exception as e:
        st.error(f"Error fetching resources: {str(e)}")

    st.subheader("➕ Add New Resource")
    with st.form("add_resource"):
        # Info needed to add a new resource
        res_title = st.text_input("Title")
        res_url = st.text_input("URL")
        res_type = st.selectbox("Type", ["Video", "PDF", "Article", "Tool"])
        
        if st.form_submit_button("Add Resource"):
            if res_title and res_url:
                payload = {
                    "Title": res_title,
                    "URL": res_url,
                    "Type": res_type,
                    "Trainer_ID": trainer_id
                }
                
                # Use API to add a resource
                try:
                    r = requests.post(f"{BASE_URL}/resources", json=payload)
                    if r.status_code in [200, 201]:
                        st.success("Resource added successfully!")
                    else:
                        st.error(f"Failed to add resource.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Title and URL are required")