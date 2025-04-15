import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module
SideBarLinks()

# Set the header of the page
st.header('Arnold\'s Diet Planner')

# Access the session state for personalization
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}.")
else:
    st.write("### Welcome to your Diet Planner.")

# Construct API URL for meal plans
MEAL_PLANS_URL = "http://web-api:4000/n/meal-plans/31"

# Function to fetch data from API
def fetch_data(url):
    try:
        logger.info(f"Fetching data from: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error(f"Failed API call to {url} - Status: {response.status_code}")
            return None
    except Exception as e:
        logger.exception(f"Exception when fetching {url}")
        return None

# Main app
try:
    # Add a loading spinner while fetching data
    with st.spinner("Loading your diet plan..."):
        # Fetch meal plans data
        meal_plans_data = fetch_data(MEAL_PLANS_URL)
        
        if meal_plans_data and len(meal_plans_data) > 0:
            # Convert to DataFrame
            meal_plans_df = pd.DataFrame(meal_plans_data)
            
            # Display active meal plan
            st.subheader("Your Active Meal Plan")
            
            # Get the most recent meal plan
            current_plan = meal_plans_df.iloc[0]
            
            # Map column names based on SQL schema (case sensitive)
            column_mapping = {
                'calories': ['Calories', 'calories', 'CALORIES'],
                'protein_goal': ['Protein_Goal', 'protein_goal', 'PROTEIN_GOAL'],
                'carb_goal': ['Carb_Goal', 'carb_goal', 'CARB_GOAL'],
                'fat_goal': ['Fat_Goal', 'fat_goal', 'FAT_GOAL'],
                'fiber_goal': ['Fiber_Goal', 'fiber_goal', 'FIBER_GOAL'],
                'start_date': ['Start_Date', 'start_date', 'START_DATE'],
                'end_date': ['End_Date', 'end_date', 'END_DATE']
            }
            
            # Function to safely get a value from the plan using column mapping
            def get_plan_value(key, default="N/A"):
                for col in column_mapping.get(key, [key]):
                    if col in current_plan:
                        return current_plan[col]
                return default
            
            # Display meal plan details in a nice format
            col1, col2 = st.columns(2)
            with col1:
                calories = get_plan_value('calories')
                protein = get_plan_value('protein_goal')
                st.metric("Daily Calories", f"{calories} kcal")
                st.metric("Protein Goal", f"{protein}g")
            with col2:
                carbs = get_plan_value('carb_goal')
                fat = get_plan_value('fat_goal')
                st.metric("Carbs Goal", f"{carbs}g")
                st.metric("Fat Goal", f"{fat}g")
            
            fiber = get_plan_value('fiber_goal')
            st.metric("Fiber Goal", f"{fiber}g")
            
            # Date range
            start_date = get_plan_value('start_date')
            end_date = get_plan_value('end_date')
            
            # Format dates if they exist - fix the date order if needed
            try:
                if start_date != "N/A":
                    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
                if end_date != "N/A":
                    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
                    
                # Swap dates if they appear to be in the wrong order
                start_date_obj = pd.to_datetime(start_date)
                end_date_obj = pd.to_datetime(end_date)
                
                if start_date_obj > end_date_obj:
                    start_date, end_date = end_date, start_date
            except:
                # If date formatting fails, keep original values
                pass
                
            st.write(f"**Plan Period:** {start_date} to {end_date}")
            
            # Display nutrition goals in a chart format
            st.subheader("Nutrition Goals")
            
            # Create a bar chart of nutritional goals
            goals_data = {
                "Nutrient": ["Protein", "Carbs", "Fat", "Fiber"],
                "Goals (g)": [
                    get_plan_value('protein_goal'),
                    get_plan_value('carb_goal'),
                    get_plan_value('fat_goal'),
                    get_plan_value('fiber_goal')
                ]
            }
            
            # Convert to numeric if possible
            for i, val in enumerate(goals_data["Goals (g)"]):
                try:
                    goals_data["Goals (g)"][i] = float(val)
                except:
                    goals_data["Goals (g)"][i] = 0
            
            # Create a DataFrame for the chart
            goals_df = pd.DataFrame(goals_data)
            
            # Display the chart
            st.bar_chart(goals_df.set_index("Nutrient"))
                    
        else:
            st.info("No meal plans found. Please check with your nutritionist to create a meal plan.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    logger.exception("Unexpected exception in diet planner app")