import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.header("💬 Message Board")
st.write(f"Welcome, {st.session_state['first_name']}!")

BASE_URL = "http://web-api:4000/t"

# Button to navigate back to trainer dashboard
col1, col2, col3 = st.columns([8, 1, 1])
with col3:
    if st.button("⬅️ Back"):
        st.switch_page('pages/31_trainer_home.py') 

st.subheader("Select Client")
client_id = st.text_input("Enter Client ID:", "1")

# Tabs for sending messages and message templates
tab1, tab2 = st.tabs(["Send Message", "Message Templates"])
with tab1:
    st.subheader("Send Message")
    # Form for sending a message
    trainer_id = st.text_input("Trainer ID:", st.session_state.get('user_id', '1'))
    message_type = st.selectbox("Message Type:", ["General", "Workout", "Schedule", "Motivation", "Nutrition"])
    message = st.text_area("Message:", st.session_state.get("current_template", ""))

    if st.button("Send Message") and message:
        try:
            # Format message with type
            formatted_message = f"[{message_type}] {message}"
            
            # Prepare data
            message_data = {
                "trainer_id": trainer_id,
                "content": formatted_message
            }
            
            # Send message through API
            response = requests.post(f"{BASE_URL}/message/{client_id}", json=message_data)
            
            if response.ok:
                st.success("Message sent successfully!")
            else:
                st.error("Failed to send message.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Message Templates")
    st.write("**Quick Templates**")
    templates = {
        "Workout Reminder": "Don't forget about our session tomorrow at [time]. Bring water and comfortable clothes.",
        "Progress Update": "Great work this week! I've noticed improvement in your [exercise] form.",
        "Schedule Change": "I need to reschedule our session on [date]. Would [new time] work for you?",
        "Motivation": "Keep up the great work! Remember that consistency is key to reaching your goals.",
        "Check-in": "How are you feeling after yesterday's workout? Any soreness or questions?"
    }

    # Display templates with copy buttons
    for title, template in templates.items():
        st.write(f"**{title}**")
        st.code(template)
        if st.button(f"Use this template", key=title):
            st.session_state['current_template'] = template
            st.rerun()

    # Handle template selection (will appear in the text area)
    if 'current_template' in st.session_state:
        st.info(f"Template loaded. Go to 'Send Message' tab to edit and send.")