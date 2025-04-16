import streamlit as st
import requests
from modules.nav import SideBarLinks


SideBarLinks()


st.header("📋 Meal Plans Manager")
st.write(f"### Welcome, {st.session_state['first_name']}!")


client_id = st.text_input("Enter Client ID:", "1")

BASE_URL = "http://web-api:4000/n"

# Create Meal Plan 
st.subheader("🆕 Create New Meal Plan")
end_date = st.date_input("End Date for Meal Plan")
if st.button("Create Meal Plan"):
    payload = {"End_Date": str(end_date)}
    resp = requests.post(f"{BASE_URL}/meal-plans/{client_id}", json=payload)
    if resp.status_code == 201:
        st.success("Meal plan created successfully!")
    else:
        st.error("Failed to create meal plan.")

# Update Meal Plan 
st.subheader("✏️ Update Existing Meal Plan")
plan_id_to_update = st.text_input("Enter Plan ID to update")
fiber = st.number_input("Fiber Goal", min_value=0)
fat = st.number_input("Fat Goal", min_value=0)
carbs = st.number_input("Carb Goal", min_value=0)
protein = st.number_input("Protein Goal", min_value=0)
calories = st.number_input("Calorie Goal", min_value=0)

if st.button("Update Meal Plan") and plan_id_to_update:
    update_payload = {
        "Plan_ID": plan_id_to_update,
        "Fiber_Goal": fiber,
        "Fat_Goal": fat,
        "Carb_Goal": carbs,
        "Protein_Goal": protein,
        "Calories": calories
    }
    resp = requests.put(f"{BASE_URL}/meal-plans/{client_id}", json=update_payload)
    if resp.status_code == 200:
        st.success("Meal plan updated successfully!")
    else:
        st.error("Failed to update meal plan.")

# Delete Meal Plan 
st.subheader("🗑️ Delete Meal Plan")
plan_id_to_delete = st.text_input("Enter Plan ID to delete")
if st.button("Delete Meal Plan") and plan_id_to_delete:
    resp = requests.delete(f"{BASE_URL}/meal-plans/{client_id}?plan_id={plan_id_to_delete}")
    if resp.status_code == 200:
        st.success("Meal plan deleted successfully!")
    else:
        st.error("Failed to delete meal plan.")

# View Meal Plans 
st.subheader("📄 View All Meal Plans")
if st.button("Load Meal Plans"):
    resp = requests.get(f"{BASE_URL}/meal-plans/{client_id}")
    if resp.ok:
        meal_plans = resp.json()
        if meal_plans:
            st.dataframe(meal_plans)
        else:
            st.info("No meal plans found.")
    else:
        st.error("Failed to fetch meal plans.")
