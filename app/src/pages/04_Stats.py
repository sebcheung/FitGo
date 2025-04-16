import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Health Metrics Dashboard')
if 'first_name' in st.session_state:
    st.write(f"### Client: {st.session_state['first_name']}")
METRICS_URL = f"http://web-api:4000/t/health_metrics/33"

# Create tabs
tab1, tab2, tab3 = st.tabs(["View", "Add", "Update"])

with tab1:
    # Fetch and display metrics
    try:
        response = requests.get(METRICS_URL, timeout=5)
        if response.status_code == 200 and response.json():
            metrics_df = pd.DataFrame(response.json())
            if 'Date' in metrics_df.columns:
                metrics_df['Date'] = pd.to_datetime(metrics_df['Date'])
            
            # Summary stats
            cols = st.columns(3)
            cols[0].metric("Avg Heart Rate", f"{metrics_df['Heart_Rate'].mean():.0f} bpm")
            cols[1].metric("Avg Sleep", f"{metrics_df['Sleep_Duration'].mean():.1f} hrs")
            cols[2].metric("Avg Calories Burned", f"{metrics_df['Calories_Burned'].mean():.0f}")
            
            # Recent data
            st.subheader("Recent Metrics")
            st.dataframe(metrics_df.sort_values('Date', ascending=False).head(5))
            
            # Basic chart
            st.subheader("Heart Rate Trend")
            fig = px.line(metrics_df.sort_values('Date'), x='Date', y='Heart_Rate')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No health metrics found.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Add New Health Metrics")
    
    with st.form("add_health_form"):
        col1, col2 = st.columns(2)
        with col1:
            heart_rate = st.number_input("Heart Rate (BPM)", 40, 250, 70)
            blood_pressure = st.selectbox("Blood Pressure", ["Normal", "Elevated"])
            sleep = st.number_input("Sleep (hours)", 0, 24, 8)
        with col2:
            calories_burned = st.number_input("Calories Burned", 0, 5000, 1800)
            water = st.number_input("Water Intake (L)", 0.0, 20.0, 2.0, step=0.1)
            calories_consumed = st.number_input("Calories Consumed", 0, 10000, 2000)
            body_fat = st.number_input("Body Fat %", 0.0, 100.0, 15.0, step=0.1)
        
        if st.form_submit_button("Submit"):
            data = {
                "User_ID": 33,
                "Heart_Rate": heart_rate,
                "Blood_Pressure_Level": blood_pressure,
                "Sleep_Duration": sleep,
                "Calories_Burned": calories_burned,
                "Water_Intake": water,
                "Caloric_Intake": calories_consumed,
                "Body_Fat_Percentage": body_fat
            }
            
            try:
                response = requests.post(METRICS_URL, json=data)
                if response.status_code == 201:
                    st.success("Health metrics added successfully!")
                else:
                    st.error(f"Error adding metrics. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab3:
    st.subheader("Update Health Metrics")
    
    try:
        response = requests.get(METRICS_URL, timeout=5)
        if response.status_code == 200 and response.json():
            metrics_df = pd.DataFrame(response.json())
            
            # Select record to update
            record_id = st.selectbox(
                "Select Record", 
                options=metrics_df['Record_ID'].tolist(),
                format_func=lambda x: f"Record #{x} - {pd.to_datetime(metrics_df[metrics_df['Record_ID']==x]['Date'].values[0]).strftime('%Y-%m-%d')}"
            )
            
            if record_id:
                record = metrics_df[metrics_df['Record_ID'] == record_id].iloc[0]
                
                with st.form("update_form"):
                    heart_rate = st.number_input("Heart Rate", 40, 250, int(record['Heart_Rate']))
                    calories_burned = st.number_input("Calories Burned", 0, 5000, int(record['Calories_Burned']))
                    
                    if st.form_submit_button("Update"):
                        update_data = {
                            "Record_ID": record_id,
                            "Heart_Rate": heart_rate,
                            "Calories_Burned": calories_burned
                        }
                        
                        try:
                            response = requests.put(f"{METRICS_URL}/{record_id}", json=update_data)
                            if response.status_code == 200:
                                st.success("Health metrics updated successfully!")
                            else:
                                st.error(f"Error updating metrics. Status code: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.warning("No health metrics found to update.")
    except Exception as e:
        st.error(f"Error: {str(e)}")