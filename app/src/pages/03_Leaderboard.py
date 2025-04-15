import logging
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.express as px

# Set up basic page
SideBarLinks()
st.header('FitGo Leaderboard 🏆')

# Current user ID
CURRENT_USER_ID = 33

# Access the session state for personalization
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}!")

# API endpoint
LEADERBOARD_URL = "http://web-api:4000/c/leaderboard"

# Fetch leaderboard data
try:
    with st.spinner("Loading leaderboard data..."):
        response = requests.get(LEADERBOARD_URL, timeout=5)
        
        if response.status_code == 200:
            leaderboard_data = response.json()
            leaderboard_df = pd.DataFrame(leaderboard_data)
            
            # Rename columns for clarity
            if 'Total_Points' in leaderboard_df.columns:
                leaderboard_df.rename(columns={'Total_Points': 'Points', 'Ranks': 'Rank'}, inplace=True)
            
            # Mark current user
            leaderboard_df['IsCurrentUser'] = leaderboard_df['User_ID'] == CURRENT_USER_ID
            
            # Create tabs
            tab1, tab2 = st.tabs(["Rankings", "Regions"])
            
            with tab1:
                # Sort by points (descending)
                sorted_df = leaderboard_df.sort_values(by='Points', ascending=False)
                
                # Create bar chart for top 10
                fig = px.bar(
                    sorted_df.head(10),
                    x='Username',
                    y='Points',
                    color='IsCurrentUser',
                    color_discrete_map={True: '#ff9933', False: '#1f77b4'},
                    title='Top 10 Users by Points'
                )
                st.plotly_chart(fig)
                
                # Display table with highlighting
                st.subheader("Leaderboard Rankings")
                st.dataframe(
                    sorted_df.style.apply(
                        lambda x: ['background-color: #ffddbb' if x['IsCurrentUser'] else '' for _ in x],
                        axis=1
                    ),
                    use_container_width=True,
                    hide_index=True,
                    column_order=['Username', 'Rank', 'Points', 'Region']
                )
            
            with tab2:
                # Show regions with data
                regions_df = leaderboard_df[leaderboard_df['Region'].notna()]
                
                if len(regions_df) > 0:
                    # Group by region
                    region_stats = regions_df.groupby('Region').agg(
                        Users=('Username', 'count'),
                        Avg_Points=('Points', 'mean')
                    ).reset_index()
                    
                    # Display region chart
                    region_fig = px.bar(
                        region_stats,
                        x='Region',
                        y='Avg_Points',
                        title='Average Points by Region'
                    )
                    st.plotly_chart(region_fig)
                    
                    # Display region stats
                    st.dataframe(region_stats, use_container_width=True)
                else:
                    st.info("No regional data available")
        else:
            st.error(f"Could not load leaderboard data (Error {response.status_code})")
except Exception as e:
    st.error(f"Error: {str(e)}")