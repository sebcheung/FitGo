import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks()

# Page header and user greeting
st.header("Client Overview")
st.write(f"### Welcome, {st.session_state['first_name']}!")

# Input for selecting client
client_id = st.text_input("Enter Client ID to view health & nutrition data:", "1")

BASE_URL = "http://web-api:4000/n"

if st.button("Load Client Data"):
    # ----------------- Meal Plans -----------------
    meal_res = requests.get(f"{BASE_URL}/meal-plans/{client_id}")
    if meal_res.ok:
        st.subheader("📋 Meal Plans")
        meal_plans_df = pd.DataFrame(meal_res.json())
        st.dataframe(meal_plans_df)
    else:
        st.error("Could not fetch meal plans.")

    # ----------------- Meal Logs ------------------
    logs_res = requests.get(f"{BASE_URL}/meals_logs/{client_id}")
    if logs_res.ok:
        st.subheader("📊 Meal Logs")
        meal_logs_df = pd.DataFrame(logs_res.json())
        st.dataframe(meal_logs_df)

        # --------- Add Simple Graph (Calories Over Time) ---------
        if 'Time' in meal_logs_df.columns and 'Calories' in meal_logs_df.columns:
            meal_logs_df['Time'] = pd.to_datetime(meal_logs_df['Time'])
            fig = px.line(meal_logs_df, x='Time', y='Calories', title='Calories Logged Over Time')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Could not fetch meal logs.")

    # ----------------- Restrictions ------------------
    rest_res = requests.get(f"{BASE_URL}/restrictions/{client_id}")
    if rest_res.ok:
        st.subheader("🚫 Dietary Restrictions")
        st.table(pd.DataFrame(rest_res.json()))
    else:
        st.error("Could not fetch restrictions.")

    # ----------------- Educational Content ------------------
    edu_res = requests.get(f"{BASE_URL}/educational-content/{client_id}")
    if edu_res.ok:
        st.subheader("📚 Educational Resources")
        for item in edu_res.json():
            st.markdown(f"**{item['Title']}** ({item['Type']}): [Link]({item['URL']})")
    else:
        st.error("Could not fetch educational content.")
