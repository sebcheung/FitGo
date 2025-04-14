import streamlit as st
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks()

# Page header and welcome message
st.header("🏋️ Trainer Dashboard")
st.write(f"### Welcome, {st.session_state['first_name']}!")

# Main navigation cards
st.write("### Your Trainer Portal")
st.write("Select a page to manage your clients and training activities:")

# Columns for nav cards
col1, col2, col3 = st.columns(3)

# Workout plans nav card
with col1:
    st.markdown("""
        <div style="padding: 20px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 180px;">
            <h1 style="font-size: 36px; margin-bottom: 10px;">💪</h1?
            <h3 style="margin-top: 0;">Workout Plans</h3>
                <p>Create and manage personalized exercise programs</p>
                <a href="workout_plans" target="_self">Go to Workout Plans →</a>
        </div>
    """, unsafe_allow_html=True)

# Calendar nav card
with col2:
    st.markdown("""
        <div style="padding: 20px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 180px;">
            <h1 style="font-size: 36px; margin-bottom: 10px;">📅</h1?
            <h3 style="margin-top: 0;">Training Calendar</h3>
                <p>Schedule and manage your client sessions</p>
                <a href="training_calendar" target="_self">Go to Calendar →</a>
        </div>
    """, unsafe_allow_html=True)

# Message board nav card
with col3:
    st.markdown("""
        <div style="padding: 20px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 180px;">
            <h1 style="font-size: 36px; margin-bottom: 10px;">💬</h1?
            <h3 style="margin-top: 0;">Message Board</h3>
                <p>Stay connected with your clients</p>
                <a href="message_board" target="_self">Go to Messages →</a>
        </div>
    """, unsafe_allow_html=True)

# Page descriptions
st.write("### What You Can Do")

with st.expander("💪 Workout Plans"):
    st.write("""
            On the Workout Plans page, you can: 
             - Create customized workout plans for each client
             - View and update existing workout programs
             - Track client progress metrics 
            """)
    
with st.expander("📅 Training Calendar"):
    st.write("""
            On the Training Calendar page, you can:
             - View your weekly training schedule
             - Add new training sessions for clients
             - Cancel or reschedule existing sessions
             - Manage your availability efficiently
            """)
    
with st.expander("💬 Message Board"):
    st.write("""
            On the Message Board page, you can:
             - Send personalized messages to clients
             - Use message templates for quick communication
             - View client activity and engagement
             - Provide motivation and feedback between sessions
            """)