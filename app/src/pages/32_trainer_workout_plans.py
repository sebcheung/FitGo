import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

# Page header
st.header("💪 Workout Plans")
st.write(f"Welcome, {st.session_state['first_name']}!")

BASE_URL = "http://web-api:4000/t"

# Button to navigate back to trainer dashboard
col1, col2, col3 = st.columns([8, 1, 1])
with col3:
    if st.button("⬅️ Back"):
        st.switch_page('pages/31_trainer_home.py') 

# Client selection
st.subheader("Select Client")
client_id = st.text_input("Enter Client ID:", "1")

# Tabs to view/create/update a plan
tab1, tab2, tab3 = st.tabs(["View Plans", "Create Plan", "Update Plan"])
with tab1:
    st.subheader("Current Workout Plan")
    if st.button("View Workout Plan"):
        try:
            # Fetch workout plan
            response = requests.get(f"{BASE_URL}/workout_plans/{client_id}")
            
            if response.ok:
                plans = response.json()
                if plans:
                    plan = plans[0]  # Show the first plan
                    st.write(f"**Goal:** {plan.get('Goal', 'N/A')}")
                    st.write(f"**Duration:** {plan.get('Duration', 'N/A')} weeks")
                    st.write("**Exercises:**")
                    
                    # Display exercises
                    exercises = plan.get('Exercise_List', '')
                    if isinstance(exercises, str):
                        exercises = exercises.split(',')
                    
                    for ex in exercises:
                        st.write(f"• {ex.strip()}")
                    
                    # Delete option
                    if st.button("Delete This Plan"):
                        delete_resp = requests.delete(f"{BASE_URL}/workout_plans/{client_id}")
                        if delete_resp.ok:
                            st.success("Plan deleted successfully!")
                else:
                    st.info("No workout plan found for this client.")
            else:
                st.error("Failed to fetch workout plan. Status code: {response.status_code}")
                st.error(f"Response: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Create New Plan")
    # Form for creating a workout plan
    trainer_id = st.text_input("Trainer ID:", st.session_state.get('user_id', '1'))
    goal = st.selectbox("Goal:", ["Weight Loss", "Muscle Gain", "Endurance", "Strength", "Flexibility"])
    duration = st.number_input("Duration (weeks):", min_value=1, max_value=52, value=8)
    exercises = st.text_area("Exercises (comma-separated):", "Squats, Deadlifts, Bench Press, Pull-ups")

    if st.button("Create Plan"):
        try:
            # Prepare data
            plan_data = {
                "trainer_id": trainer_id,
                "goal": goal,
                "exercise_list": exercises,
                "duration": duration
            }
            
            # Create plan through API
            response = requests.post(f"{BASE_URL}/workout_plans/{client_id}", json=plan_data)
            
            if response.ok:
                st.success("Workout plan created successfully!")
            else:
                st.error("Failed to create workout plan. Status code: {response.status_code}")
                st.error(f"Response: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab3:
    st.subheader("Update Existing Plan")
    # Form for updating a workout plan
    new_goal = st.selectbox("New Goal:", ["", "Weight Loss", "Muscle Gain", "Endurance", "Strength", "Flexibility"])
    new_duration = st.number_input("New Duration (weeks):", min_value=1, max_value=52, value=8)
    new_exercises = st.text_area("New Exercises (comma-separated):", "")

    if st.button("Update Plan"):
        try:
            # Prepare data (only include non empty fields)
            update_data = {}
            if new_goal:
                update_data["goal"] = new_goal
            if new_duration:
                update_data["duration"] = new_duration
            if new_exercises:
                update_data["exercise_list"] = new_exercises
                
            if update_data:
                # Update plan through API
                response = requests.put(f"{BASE_URL}/workout_plans/{client_id}", json=update_data)
                
                if response.ok:
                    st.success("Workout plan updated successfully!")
                else:
                    st.error("Failed to update workout plan. Status code: {response.status_code}")
                    st.error(f"Response: {response.text}")
            else:
                st.warning("No changes specified to update.")
        except Exception as e:
            st.error(f"Error: {str(e)}")