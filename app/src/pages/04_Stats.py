import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Health Metrics Dashboard')
if 'first_name' in st.session_state:
    st.write(f"### Client: {st.session_state['first_name']}")

# API endpoint 
METRICS_URL = "http://web-api:4000/t/health_metrics/33"

# Fetch health metrics data
try:
    with st.spinner("Loading health metrics..."):
        response = requests.get(METRICS_URL, timeout=5)
        
        if response.status_code == 200:
            metrics_data = response.json()
            
            if metrics_data:
                # Convert to DataFrame
                metrics_df = pd.DataFrame(metrics_data)
                
                # Convert date to datetime if needed
                if 'Date' in metrics_df.columns:
                    metrics_df['Date'] = pd.to_datetime(metrics_df['Date'])
                
                # Create tabs for different metrics
                tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Cardiovascular", "Nutrition", "Sleep"])
                
                with tab1:
                    st.subheader("Health Metrics Overview")
                    
                    # Summary statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        avg_heart_rate = metrics_df['Heart_Rate'].mean()
                        st.metric("Avg. Heart Rate", f"{avg_heart_rate:.0f} bpm")
                        
                    with col2:
                        avg_sleep = metrics_df['Sleep_Duration'].mean()
                        st.metric("Avg. Sleep", f"{avg_sleep:.1f} hrs")
                        
                    with col3:
                        avg_calories_burned = metrics_df['Calories_Burned'].mean()
                        st.metric("Avg. Calories Burned", f"{avg_calories_burned:.0f}")
                    
                    # Recent metrics table
                    st.subheader("Recent Metrics")
                    recent_df = metrics_df.sort_values('Date', ascending=False).head(5)
                    st.dataframe(recent_df, use_container_width=True)
                
                with tab2:
                    st.subheader("Cardiovascular Health")
                    
                    # Heart rate over time
                    fig = px.line(
                        metrics_df.sort_values('Date'), 
                        x='Date', 
                        y='Heart_Rate',
                        title='Heart Rate Over Time'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Blood pressure distribution
                    bp_counts = metrics_df['Blood_Pressure_Level'].value_counts().reset_index()
                    bp_counts.columns = ['Blood Pressure Level', 'Count']
                    
                    fig2 = px.pie(
                        bp_counts,
                        values='Count',
                        names='Blood Pressure Level',
                        title='Blood Pressure Level Distribution'
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # Calories burned
                    fig3 = px.bar(
                        metrics_df.sort_values('Date').tail(10),
                        x='Date',
                        y='Calories_Burned',
                        title='Recent Calories Burned'
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                with tab3:
                    st.subheader("Nutrition Metrics")
                    
                    # Water intake over time
                    fig = px.line(
                        metrics_df.sort_values('Date'),
                        x='Date',
                        y='Water_Intake',
                        title='Water Intake Over Time (L)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Caloric intake vs burned
                    recent_df = metrics_df.sort_values('Date').tail(7)
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(
                        x=recent_df['Date'],
                        y=recent_df['Caloric_Intake'],
                        name='Calories Consumed',
                        marker_color='blue'
                    ))
                    fig2.add_trace(go.Bar(
                        x=recent_df['Date'],
                        y=recent_df['Calories_Burned'],
                        name='Calories Burned',
                        marker_color='red'
                    ))
                    fig2.update_layout(
                        title='Caloric Balance (Last 7 Records)',
                        barmode='group'
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # Body fat percentage
                    fig3 = px.line(
                        metrics_df.sort_values('Date'),
                        x='Date',
                        y='Body_Fat_Percentage',
                        title='Body Fat Percentage Over Time'
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                with tab4:
                    st.subheader("Sleep Patterns")
                    
                    # Sleep duration over time
                    fig = px.bar(
                        metrics_df.sort_values('Date'),
                        x='Date',
                        y='Sleep_Duration',
                        title='Sleep Duration Over Time (hours)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Sleep quality metrics
                    avg_sleep = metrics_df['Sleep_Duration'].mean()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Average Sleep", f"{avg_sleep:.1f} hours")
                    with col2:
                        sleep_quality = "Good" if avg_sleep >= 7 else "Poor"
                        st.metric("Sleep Quality", sleep_quality)
                    
                    # Sleep recommendation
                    if avg_sleep < 7:
                        st.warning("Client is not getting enough sleep. The recommended amount is 7-9 hours.")
                    elif avg_sleep > 9:
                        st.info("Client is getting more than the recommended 7-9 hours of sleep.")
                    else:
                        st.success("Client is getting the recommended 7-9 hours of sleep.")
            else:
                st.warning("No health metrics found for this client.")
        else:
            st.error(f"Failed to fetch health metrics. Status code: {response.status_code}")
            
except Exception as e:
    st.error(f"Error: {str(e)}")