import streamlit as st
import requests
from modules.nav import SideBarLinks

# Add sidebar navigation
SideBarLinks()

# Page header and user greeting
st.header("🚫 Restrictions Manager")
st.write(f"### Welcome, {st.session_state['first_name']}!")

# Ask for client ID
client_id = st.text_input("Enter Client ID:", "1")

BASE_URL = "http://web-api:4000/n"

#Add Restriction 
st.subheader("➕ Add a New Restriction")
new_rest = st.text_input("Enter new restriction")
if st.button("Add Restriction") and new_rest:
    resp = requests.post(f"{BASE_URL}/restrictions/{client_id}", json={"restriction": new_rest})
    if resp.status_code == 201:
        st.success("Restriction added successfully!")
    else:
        st.error("Failed to add restriction.")

# Delete Restriction
st.subheader("❌ Delete an Existing Restriction")
delete_rest = st.text_input("Enter restriction to delete")
if st.button("Delete Restriction") and delete_rest:
    resp = requests.delete(f"{BASE_URL}/restrictions/{client_id}?restriction={delete_rest}")
    if resp.status_code == 200:
        st.success("Restriction deleted successfully!")
    else:
        st.error("Failed to delete restriction.")

# ----------------- View Current Restrictions ------------------
st.subheader("📋 Current Restrictions")
if st.button("View Restrictions"):
    resp = requests.get(f"{BASE_URL}/restrictions/{client_id}")
    if resp.ok:
        restrictions = resp.json()
        if restrictions:
            st.table(restrictions)
        else:
            st.info("No restrictions found for this client.")
    else:
        st.error("Failed to fetch restrictions.")
