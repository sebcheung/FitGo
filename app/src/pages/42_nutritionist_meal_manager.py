import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

st.header("🍽️ Meals Manager")
st.write(f"### Welcome, {st.session_state['first_name']}!")

BASE_URL = "http://web-api:4000/n"

# View Meals 
st.subheader("📄 View All Meals")
if st.button("Load Meals"):
    resp = requests.get(f"{BASE_URL}/meals")
    if resp.ok:
        meals = resp.json()
        if meals:
            st.dataframe(pd.DataFrame(meals))
        else:
            st.info("No meals found.")
    else:
        st.error("Failed to fetch meals.")

# Add Meal 
st.subheader("➕ Add New Meal")
meal_plan_id = st.text_input("Meal Plan ID")
meal_name = st.text_input("Meal Name")
meal_type = st.text_input("Meal Type")
meal_recipe = st.text_area("Meal Recipe")
meal_ingredients = st.text_area("Meal Ingredients")
if st.button("Add Meal"):
    payload = {
        "Plan_ID": meal_plan_id,
        "Name": meal_name,
        "Type": meal_type,
        "Recipe": meal_recipe,
        "Ingredients": meal_ingredients
    }
    resp = requests.post(f"{BASE_URL}/meals", json=payload)
    if resp.status_code == 201:
        st.success("Meal added successfully!")
    else:
        st.error("Failed to add meal.")

# Update Meal 
st.subheader("✏️ Update Meal")
meal_id = st.text_input("Meal ID to update")
up_name = st.text_input("Updated Name")
up_type = st.text_input("Updated Type")
up_recipe = st.text_area("Updated Recipe")
up_ingredients = st.text_area("Updated Ingredients")
if st.button("Update Meal") and meal_id:
    payload = {
        "Meal_ID": meal_id,
        "Name": up_name,
        "Type": up_type,
        "Recipe": up_recipe,
        "Ingredients": up_ingredients
    }
    resp = requests.put(f"{BASE_URL}/meals", json=payload)
    if resp.status_code == 200:
        st.success("Meal updated successfully!")
    else:
        st.error("Failed to update meal.")

# Delete Meal 
st.subheader("🗑️ Delete Meal")
meal_id_delete = st.text_input("Meal ID to delete")
if st.button("Delete Meal") and meal_id_delete:
    resp = requests.delete(f"{BASE_URL}/meals?meal_id={meal_id_delete}")
    if resp.status_code == 200:
        st.success("Meal deleted successfully!")
    else:
        st.error("Failed to delete meal.")