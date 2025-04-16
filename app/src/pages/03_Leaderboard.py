import logging
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.express as px

SideBarLinks()
st.header('FitGo Leaderboard 🏆')
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}!")

# API endpoint for current user
USER_LEADERBOARD_URL = "http://web-api:4000/c/leaderboard/33"

# Create dataframe with leaderboard entries from sample data
leaderboard_data = [
    {"Leaderboard_ID": 21, "User_ID": 33, "Username": "FitFan123", "Ranks": 16, "Total_Points": 389, "Region": "Colorado"},
    {"Leaderboard_ID": 1, "User_ID": 35, "Username": "PowerLifter404", "Ranks": 25, "Total_Points": 668, "Region": "Guarda"},
    {"Leaderboard_ID": 2, "User_ID": 39, "Username": "GymGuru456", "Ranks": 12, "Total_Points": 841, "Region": "Lisboa"},
    {"Leaderboard_ID": 3, "User_ID": 10, "Username": "YogaYogi505", "Ranks": 20, "Total_Points": 387, "Region": "Lisboa"},
    {"Leaderboard_ID": 4, "User_ID": 24, "Username": "RunRanger606", "Ranks": 23, "Total_Points": 843, "Region": "Porto"},
    {"Leaderboard_ID": 5, "User_ID": 12, "Username": "MuscleManiac101", "Ranks": 33, "Total_Points": 557, "Region": "Lisbon"},
    {"Leaderboard_ID": 14, "User_ID": 14, "Username": "SweatSquad789", "Ranks": 2, "Total_Points": 751, "Region": "Porto"},
    {"Leaderboard_ID": 28, "User_ID": 2, "Username": "CardioQueen202", "Ranks": 13, "Total_Points": 841, "Region": "Michigan"},
    {"Leaderboard_ID": 45, "User_ID": 5, "Username": "IronWarrior707", "Ranks": 16, "Total_Points": 988, "Region": "Barcelona"}
]

# Convert to DataFrame and rename columns
leaderboard_df = pd.DataFrame(leaderboard_data)
leaderboard_df.rename(columns={'Total_Points': 'Points', 'Ranks': 'Rank'}, inplace=True)

# Mark current user
leaderboard_df['IsCurrentUser'] = leaderboard_df['User_ID'] == 33

# Try to get current user data from API
try:
    response = requests.get(USER_LEADERBOARD_URL, timeout=5)
    
    if response.status_code == 200:
        current_user_data = response.json()
        if current_user_data and isinstance(current_user_data, list) and len(current_user_data) > 0:
            # Replace the user data in our dataframe with API data
            leaderboard_df = leaderboard_df[leaderboard_df['User_ID'] != 33]
            
            # Add API data for current user
            for user_entry in current_user_data:
                # Rename keys to match our DataFrame
                if 'Total_Points' in user_entry:
                    user_entry['Points'] = user_entry.pop('Total_Points')
                if 'Ranks' in user_entry:
                    user_entry['Rank'] = user_entry.pop('Ranks')
                user_entry['IsCurrentUser'] = True
                
                # Add to DataFrame
                leaderboard_df = pd.concat([leaderboard_df, pd.DataFrame([user_entry])], ignore_index=True)
except Exception as e:
    st.sidebar.warning(f"Could not fetch your data: {str(e)}")

# Create tabs
tab1, tab2 = st.tabs(["Rankings", "Regions"])

with tab1:
    # Sort by points (descending)
    sorted_df = leaderboard_df.sort_values(by='Points', ascending=False)
    
    # Find current user's position
    user_position = sorted_df.reset_index().index[sorted_df['IsCurrentUser']].tolist()
    user_position = user_position[0] + 1 if user_position else None
    
    if user_position:
        st.success(f"Your position in the leaderboard: #{user_position}")
    
    # Create bar chart for top 10
    fig = px.bar(
        sorted_df.head(10),
        x='Username',
        y='Points',
        color='IsCurrentUser',
        color_discrete_map={True: '#ff9933', False: '#1f77b4'},
        title='Top 10 Users by Points'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display table with highlighting
    st.subheader("Leaderboard Rankings")
    
    # Use st.dataframe with styling to highlight current user
    styled_df = sorted_df[['Username', 'Rank', 'Points', 'Region']]
    st.dataframe(
        styled_df.style.apply(
            lambda x: ['background-color: #ffddbb' if sorted_df.iloc[x.name]['IsCurrentUser'] else '' for _ in range(len(x))],
            axis=1
        ),
        use_container_width=True,
        hide_index=True
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
        st.plotly_chart(region_fig, use_container_width=True)
        
        # Find user's region
        user_region = leaderboard_df.loc[leaderboard_df['IsCurrentUser'], 'Region'].values
        if len(user_region) > 0 and pd.notna(user_region[0]):
            st.info(f"Your region: {user_region[0]}")
        
        # Display region stats
        st.dataframe(region_stats, use_container_width=True)
    else:
        st.info("No regional data available")