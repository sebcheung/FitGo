import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# Set up basic page
SideBarLinks()
st.header('Health Metrics Dashboard')

# Current client ID
CLIENT_ID = 33

# Access the session state for personalization
if 'first_name' in st.session_state:
    st.write(f"### Client: {st.session_state['first_name']}")

# API endpoint - note the /t prefix for trainer routes
METRICS_URL = f"http://web-api:4000/t/health_metrics/{CLIENT_ID}"

# Debug info
with st.expander("Debug Info"):
    st.write(f"Attempting to connect to: {METRICS_URL}")

try:
    # Attempt the API call
    with st.spinner("Connecting to API..."):
        try:
            response = requests.get(METRICS_URL, timeout=5)
            st.write(f"API Response status: {response.status_code}")
            
            # Try to get error details if available
            if response.status_code != 200:
                try:
                    error_details = response.json()
                    st.write(f"Error details: {error_details}")
                except:
                    st.write("No detailed error information available")
        except Exception as connection_error:
            st.error(f"API connection error: {str(connection_error)}")
    
    # Check for server connection issue
    route_parts = METRICS_URL.split('/')
    if len(route_parts) >= 4:
        # Show possible correct route
        possible_routes = [
            f"{'/'.join(route_parts[:-2])}/health_metrics/{route_parts[-1]}",
            f"{'/'.join(route_parts[:-2])}/health-metrics/{route_parts[-1]}",
            f"{'/'.join(route_parts[:-2])}/client_health_metrics/{route_parts[-1]}"
        ]
        
        st.error("The API route might be incorrect. Here are some possible routes to check:")
        for route in possible_routes:
            st.code(route)
    
    # Show route instructions
    st.info("Ensure your Flask API has the following route correctly implemented:")
    st.code("""
    @trainers.route('/health_metrics/<clientID>', methods=['GET'])
    def get_health_metrics(clientID):
        current_app.logger.info('GET /health_metrics/<clientID> route')
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM health_metrics WHERE User_ID = %s', (clientID,))
        data = cursor.fetchall()
        response = make_response(jsonify(data))
        response.status_code = 200
        return response
    """)
    
    # Display placeholder visualizations
    st.subheader("Health Metrics Placeholder")
    st.write("This visualization will populate with real data once the API is functioning correctly.")
    
    # Sample placeholder visualization
    placeholder_data = {
        'Date': pd.date_range(start='2023-01-01', periods=7),
        'Heart_Rate': [75, 78, 72, 80, 70, 75, 73],
        'Calories_Burned': [1800, 2200, 1950, 2100, 1750, 1900, 2000]
    }
    placeholder_df = pd.DataFrame(placeholder_data)
    
    # Sample plot
    fig = px.line(
        placeholder_df, 
        x='Date', 
        y='Heart_Rate',
        title='Example Heart Rate Chart (Placeholder)',
        labels={'Heart_Rate': 'Heart Rate (bpm)', 'Date': 'Date'}
    )
    fig.add_annotation(
        text="This is placeholder data. Connect to API for real metrics.",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="red")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Implementation checking
    st.subheader("Implementation Checklist")
    st.markdown("""
    - Verify the Flask API route path is correct (`/t/health_metrics/<clientID>`)
    - Check database connection in your Flask app
    - Ensure the SQL query is using the correct column name (`User_ID` not `client_id`)
    - Confirm the Health_Metrics table exists in your database
    - Check Flask logs for detailed error information
    """)
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")