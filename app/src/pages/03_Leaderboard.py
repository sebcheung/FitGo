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
API_URL = f"http://web-api:4000/c/leaderboard/33"

# Sample leaderboard data (top 10)
sample_data = [
    {'Username': 'Alice', 'Rank': 1, 'Points': 1520, 'Region': 'East'},
    {'Username': 'Bob', 'Rank': 2, 'Points': 1400, 'Region': 'West'},
    {'Username': 'Charlie', 'Rank': 3, 'Points': 1375, 'Region': 'South'},
    {'Username': 'Diana', 'Rank': 4, 'Points': 1320, 'Region': 'East'},
    {'Username': 'Evan', 'Rank': 5, 'Points': 1280, 'Region': 'North'},
    {'Username': 'Fay', 'Rank': 6, 'Points': 1250, 'Region': 'West'},
    {'Username': 'George', 'Rank': 7, 'Points': 1200, 'Region': 'East'},
    {'Username': 'Hannah', 'Rank': 8, 'Points': 1150, 'Region': 'North'},
    {'Username': 'Ian', 'Rank': 9, 'Points': 1100, 'Region': 'South'},
    {'Username': 'Jane', 'Rank': 10, 'Points': 1050, 'Region': 'West'},
]

# Fetch current user leaderboard entry
def fetch_user_entry():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                row = data[0]
                return {
                    'Username': row['Username'],
                    'Rank': row.get('Ranks', '?'),
                    'Points': row.get('Total_Points', 0),
                    'Region': row.get('Region', 'UNKNOWN'),
                    'IsCurrentUser': True
                }
    except Exception as e:
        st.warning(f"Unable to retrieve your leaderboard entry: {str(e)}")
    return None

# Build leaderboard dataframe
leaderboard_df = pd.DataFrame(sample_data)
leaderboard_df['IsCurrentUser'] = False

user_entry = fetch_user_entry()
if user_entry:
    if user_entry['Username'] not in leaderboard_df['Username'].values:
        leaderboard_df = pd.concat([leaderboard_df, pd.DataFrame([user_entry])], ignore_index=True)

leaderboard_df = leaderboard_df.sort_values(by='Points', ascending=False)

# Tabs for UI
tab1, tab2, tab3 = st.tabs(["Rankings", "Regions", "Manage Profile"])

with tab1:
    if user_entry:
        user_pos = leaderboard_df.reset_index().index[leaderboard_df['IsCurrentUser']].tolist()
        if user_pos:
            st.success(f"Your position in the leaderboard: #{user_pos[0] + 1}")

    fig = px.bar(
        leaderboard_df.head(10),
        x='Username',
        y='Points',
        color='IsCurrentUser',
        color_discrete_map={True: '#ff9933', False: '#1f77b4'},
        title='Top 10 Users by Points'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Leaderboard Rankings")
    display_df = leaderboard_df[['Username', 'Rank', 'Points', 'Region']]
    st.dataframe(
        display_df.style.apply(
            lambda row: ['background-color: #ffe0b2' if leaderboard_df.iloc[row.name]['IsCurrentUser'] else '' for _ in row],
            axis=1
        ),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    if 'Region' in leaderboard_df.columns:
        region_stats = leaderboard_df.groupby('Region').agg(
            Users=('Username', 'count'),
            Avg_Points=('Points', 'mean')
        ).reset_index()

        st.plotly_chart(
            px.bar(region_stats, x='Region', y='Avg_Points', title='Average Points by Region'),
            use_container_width=True
        )

        if user_entry:
            st.info(f"Your region: {user_entry['Region']}")

        st.dataframe(region_stats, use_container_width=True)

with tab3:
    st.subheader("Manage Your Profile")

    # Create a radio button to update profile
    action = st.radio("Select Action", ["Update My Profile", "Create New Profile"])

    if action == "Update My Profile":
        st.write("Update your leaderboard information")
        
        # Pre-fill form if user exists
        username = st.text_input("Username", 
                              value=user_entry['Username'] if user_entry else "")
        
        rank = st.number_input("Rank", 
                            min_value=1, 
                            value=int(user_entry['Rank']) if user_entry and user_entry['Rank'] != '?' else 1)
        
        points = st.number_input("Points", 
                              min_value=0, 
                              value=int(user_entry['Points']) if user_entry else 0)
        
        region = st.text_input("Region", 
                            value=user_entry['Region'] if user_entry else "")
        
        profile_pic = st.selectbox("Profile Picture", 
                               options=["profile1.jpeg", "profile2.jpeg", "profile3.jpeg", 
                                       "profile4.jpeg", "profile5.jpeg"],
                               index=0)
        
        if st.button("Update Profile"):
            # Prepare data for API
            update_data = {
                "Username": username,
                "Ranks": int(rank),
                "Total_Points": int(points),
                "Region": region,
                "Profile_Pic": profile_pic
            }
            
            try:
                # Send PUT request to update profile
                response = requests.put(API_URL, json=update_data, timeout=5)
                
                if response.status_code == 200:
                    st.success("Profile updated successfully!")
                    # Refresh the page
                    st.rerun()
                else:
                    st.error(f"Failed to update profile. Status code: {response.status_code}")
                    if hasattr(response, 'text') and response.text:
                        st.error(f"Error details: {response.text}")
            
            except Exception as e:
                st.error(f"Error updating profile: {str(e)}")
    
    # Add a section for tips
    with st.expander("Leaderboard Tips"):
        st.markdown("""
        ### Tips for climbing the leaderboard:
        
        - Complete workouts consistently to earn more points
        - Join challenges to boost your ranking
        - Connect with friends in your region for friendly competition
        - Update your profile regularly to ensure accurate ranking
        """)