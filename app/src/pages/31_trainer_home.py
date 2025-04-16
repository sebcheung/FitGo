import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.header("🏋️ Trainer Dashboard")
st.write(f"### Welcome, {st.session_state['first_name']}!")

st.write("### Your Trainer Portal")
st.write("Select a page to manage your clients and training activities:")

# Columns for nav cards
col1, col2, col3, col4 = st.columns(4)

# Workout plans nav card
with col1:
    with st.container():
        st.markdown("""
            <div style="padding: 10px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 280px;">
                <h1 style="font-size: 36px; margin-bottom: 5px;">💪</h1>
                <h3 style="margin-top: 0;">Workout Plans</h3>
                <p>Create and manage personalized exercise programs</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Workout Plans", use_container_width=True, key="plans"):
            st.switch_page('pages/32_trainer_workout_plans.py')

# Calendar nav card
with col2:
    st.markdown("""
        <div style="padding: 10px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 280px;">
            <h1 style="font-size: 36px; margin-bottom: 5px;">📅</h1>
            <h3 style="margin-top: 0;">Training Calendar</h3>
                <p>Schedule and manage your client sessions</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Calendar", use_container_width=True, key="calendar"):
            st.switch_page('pages/33_trainer_calendar.py')

# Message board nav card
with col3:
    st.markdown("""
        <div style="padding: 10px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 280px;">
            <h1 style="font-size: 36px; margin-bottom: 5px;">💬</h1>
            <h3 style="margin-top: 0;">Message Board</h3>
                <p>Stay connected with your clients</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Messages", use_container_width=True, key="messages"):
            st.switch_page('pages/34_trainer_messages.py')

# Health metrics and resources nav card
with col4:
    st.markdown("""
        <div style="padding: 10px; background-color: #f0f2f6; border-radius:10px; text-align: center; height: 280px;">
            <h1 style="font-size: 36px; margin-bottom: 5px;">🗂️</h1>
            <h3 style="margin-top: 0;">Client Resources</h3>
                <p>Look at your clients' health metrics and access resources</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Resources", use_container_width=True, key="resources"):
            st.switch_page('pages/35_trainer_resources.py')

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
    
with st.expander("🗂️ Client Resources"):
    st.write("""
            On the Client Resources page, you can:
             - View client health info
             - Create and update client health info
             - View learning tools and resources
             - Add new learning tools and resources
            """)