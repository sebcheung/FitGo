import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
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

MEAL_PLANS_URL = "http://web-api:4000/n/meal-plans/31"
MEALS_URL = "http://web-api:4000/n/meals"

# Function to fetch data from API
def fetch_data(url):
    try:
        logger.info(f"Fetching data from: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Log first record to see structure
            if isinstance(data, list) and len(data) > 0:
                logger.info(f"First record: {data[0]}")
            return data
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            logger.error(f"Failed API call to {url} - Status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        logger.exception(f"Exception when fetching {url}")
        return None

# Main app
try:
    # Add a loading spinner while fetching data
    with st.spinner("Loading your diet plans..."):
        # Fetch meal plans data
        meal_plans_data = fetch_data(MEAL_PLANS_URL)
        
        # Add debug information to sidebar
        with st.sidebar.expander("Debug: API Response"):
            st.write(meal_plans_data)
        
        if meal_plans_data and len(meal_plans_data) > 0:
            # Convert to DataFrame
            meal_plans_df = pd.DataFrame(meal_plans_data)
            
            # Show available columns for debugging
            with st.sidebar.expander("Available Columns"):
                st.write(list(meal_plans_df.columns))
            
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
                'end_date': ['End_Date', 'end_date', 'END_DATE'],
                'plan_id': ['Plan_ID', 'plan_id', 'PLAN_ID']
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
            
            # Format dates if they exist
            try:
                if start_date != "N/A":
                    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
                if end_date != "N/A":
                    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
            except:
                # If date formatting fails, keep original values
                pass
                
            st.write(f"**Plan Period:** {start_date} to {end_date}")
            
            # Fetch meals for the current plan - Get plan_id with correct capitalization
            plan_id = get_plan_value('plan_id')
            
            # Check if the correct key for meals API exists
            if plan_id != "N/A":
                # Construct meals URL
                meals_url = f"{MEALS_URL}/{plan_id}"
                
                # Log the meals URL we're about to call
                logger.info(f"Attempting to fetch meals from: {meals_url}")
                st.sidebar.info(f"Meals URL: {meals_url}")
                
                # Fetch meals data
                meals_data = fetch_data(meals_url)
                
                if meals_data and len(meals_data) > 0:
                    meals_df = pd.DataFrame(meals_data)
                    
                    # Display meals table
                    st.subheader("Meals in Your Plan")
                    
                    # Show the data regardless of column names
                    st.dataframe(meals_df, use_container_width=True)
                    
                    # Try to create visualizations if possible
                    if 'calories' in meals_df.columns and 'name' in meals_df.columns:
                        st.subheader("Calorie Distribution by Meal")
                        pie_fig = px.pie(
                            meals_df, 
                            values='calories', 
                            names='name',
                            title='Calorie Distribution'
                        )
                        st.plotly_chart(pie_fig, use_container_width=True)
                else:
                    st.info("No meals found for your current plan. Please check with your nutritionist.")
                    
                    # Show sample data for now until the meals API is fixed
                    st.subheader("Sample Meal Plan")
                    st.write("Here's what you'll see once your nutritionist adds meals to your plan:")
                    
                    sample_data = {
                        "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
                        "Calories": [400, 650, 550, 200],
                        "Protein": [20, 35, 30, 10],
                        "Carbs": [45, 65, 50, 25],
                        "Fat": [15, 25, 20, 8]
                    }
                    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)
            else:
                st.warning("Could not determine Plan ID from the data.")
        else:
            st.info("No meal plans found. Please check with your nutritionist to create a meal plan.")
            
            # Show a sample of what a meal plan would look like
            st.subheader("Sample Meal Plan")
            st.write("Once your nutritionist creates a meal plan, you'll see something like this:")
            
            # Sample data
            sample_data = {
                "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
                "Calories": [400, 650, 550, 200],
                "Protein": [20, 35, 30, 10],
                "Carbs": [45, 65, 50, 25],
                "Fat": [15, 25, 20, 8]
            }
            st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    logger.exception("Unexpected exception in diet planner app")