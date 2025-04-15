import logging
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.express as px

# Set up logging
logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module
SideBarLinks()

# Set the header of the page
st.header('FitGo Leaderboard 🏆')

# Access the session state for personalization
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}!")
else:
    st.write("### Welcome to the FitGo Leaderboard!")

# API endpoint
LEADERBOARD_URL = "http://web-api:4000/c/leaderboard"

# Function to fetch data from API
def fetch_data(url):
    try:
        logger.info(f"Fetching data from: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch data. Status code: {response.status_code}")
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        logger.exception(f"Error fetching data: {str(e)}")
        st.error(f"Error fetching data: {str(e)}")
        return None

# Main app
try:
    # Add a loading spinner while fetching data
    with st.spinner("Loading leaderboard data..."):
        leaderboard_data = fetch_data(LEADERBOARD_URL)
        
        if leaderboard_data and len(leaderboard_data) > 0:
            # Convert to DataFrame
            leaderboard_df = pd.DataFrame(leaderboard_data)
            
            # Rename columns to make them more readable (if needed)
            column_mapping = {
                'Username': 'Username',
                'Ranks': 'Rank', 
                'Total_Points': 'Points',
                'Region': 'Region',
                'Profile_Pic': 'Profile'
            }
            
            # Rename columns that exist in the dataframe
            for old_col, new_col in column_mapping.items():
                if old_col in leaderboard_df.columns:
                    leaderboard_df.rename(columns={old_col: new_col}, inplace=True)
            
            # Add rankings tab and detailed view tab
            tab1, tab2, tab3 = st.tabs(["Top Rankings", "Regional Stats", "All Users"])
            
            with tab1:
                # Sort by points and get top performers
                top_users = leaderboard_df.sort_values(by='Points', ascending=False).head(10)
                
                # Create a bar chart for top users
                fig = px.bar(
                    top_users,
                    x='Username',
                    y='Points',
                    color='Points',
                    color_continuous_scale='Viridis',
                    title='Top 10 Users by Points'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Display top users in a table
                st.subheader("Top 10 Users")
                st.dataframe(
                    top_users[['Username', 'Rank', 'Points', 'Region']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add user count and stats
                st.info(f"Total active users on leaderboard: {len(leaderboard_df)}")
                
                # Add highest achievers
                st.subheader("Highest Achievers")
                col1, col2 = st.columns(2)
                with col1:
                    # Highest points
                    highest_points = leaderboard_df.loc[leaderboard_df['Points'].idxmax()]
                    st.metric("Highest Points", highest_points['Points'], f"by {highest_points['Username']}")
                with col2:
                    # Highest rank
                    lowest_rank = leaderboard_df.loc[leaderboard_df['Rank'].astype(int).idxmin()]
                    st.metric("Top Rank", lowest_rank['Rank'], f"by {lowest_rank['Username']}")
            
            with tab2:
                # Filter out rows with null or unknown regions
                regions_df = leaderboard_df[leaderboard_df['Region'].notna() & (leaderboard_df['Region'] != 'UNKNOWN')]
                
                if len(regions_df) > 0:
                    # Group by region
                    region_stats = regions_df.groupby('Region').agg(
                        Users=('Username', 'count'),
                        Avg_Points=('Points', 'mean'),
                        Max_Points=('Points', 'max')
                    ).reset_index()
                    
                    # Create regional map or chart
                    st.subheader("Points by Region")
                    region_fig = px.bar(
                        region_stats,
                        x='Region',
                        y='Avg_Points',
                        color='Users',
                        labels={'Avg_Points': 'Average Points', 'Users': 'Number of Users'},
                        title='Average Points by Region'
                    )
                    st.plotly_chart(region_fig, use_container_width=True)
                    
                    # Display region stats
                    st.subheader("Regional Statistics")
                    st.dataframe(region_stats, use_container_width=True, hide_index=True)
                    
                    # Top region
                    top_region = region_stats.loc[region_stats['Avg_Points'].idxmax()]
                    st.success(f"🏆 Top Region: {top_region['Region']} with an average of {top_region['Avg_Points']:.1f} points per user")
                else:
                    st.info("No regional data available.")
            
            with tab3:
                # Display full leaderboard with search and filters
                st.subheader("Complete Leaderboard")
                
                # Add search and filter options
                col1, col2 = st.columns(2)
                with col1:
                    search_term = st.text_input("Search by username:")
                with col2:
                    min_points = st.slider("Minimum points:", 0, int(leaderboard_df['Points'].max()), 0)
                
                # Filter the dataframe
                filtered_df = leaderboard_df
                if search_term:
                    filtered_df = filtered_df[filtered_df['Username'].str.contains(search_term, case=False)]
                filtered_df = filtered_df[filtered_df['Points'] >= min_points]
                
                # Sort options
                sort_by = st.selectbox("Sort by:", ["Points (high to low)", "Points (low to high)", "Rank (best to worst)", "Rank (worst to best)", "Username"])
                
                if sort_by == "Points (high to low)":
                    filtered_df = filtered_df.sort_values(by='Points', ascending=False)
                elif sort_by == "Points (low to high)":
                    filtered_df = filtered_df.sort_values(by='Points', ascending=True)
                elif sort_by == "Rank (best to worst)":
                    filtered_df = filtered_df.sort_values(by='Rank', ascending=True)
                elif sort_by == "Rank (worst to best)":
                    filtered_df = filtered_df.sort_values(by='Rank', ascending=False)
                else:
                    filtered_df = filtered_df.sort_values(by='Username')
                
                # Display the filtered dataframe
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        else:
            st.warning("No leaderboard data available.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    logger.exception("Unexpected exception in leaderboard app")