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

# Construct API URLs
MEAL_PLANS_URL = "http://web-api:4000/c/meal-plans/31"
MEALS_URL = "http://web-api:4000/c/meals"

# Function to fetch data from API
def fetch_data(url):
    try:
        logger.info(f"Fetching data from: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Main app
try:
    # Add a loading spinner while fetching data
    with st.spinner("Loading your diet plans..."):
        # Fetch meal plans data
        meal_plans_data = fetch_data(MEAL_PLANS_URL)
        
        if meal_plans_data and len(meal_plans_data) > 0:
            # Convert to DataFrame
            meal_plans_df = pd.DataFrame(meal_plans_data)
            
            # Display active meal plan
            st.subheader("Your Active Meal Plan")
            
            # Format dates for better display
            if 'start_date' in meal_plans_df.columns:
                meal_plans_df['start_date'] = pd.to_datetime(meal_plans_df['start_date']).dt.strftime('%Y-%m-%d')
            if 'end_date' in meal_plans_df.columns:
                meal_plans_df['end_date'] = pd.to_datetime(meal_plans_df['end_date']).dt.strftime('%Y-%m-%d')
            
            # Get the most recent meal plan
            current_plan = meal_plans_df.iloc[0]
            
            # Display meal plan details in a nice format
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Daily Calories", f"{current_plan['calories']} kcal")
                st.metric("Protein Goal", f"{current_plan['protein_goal']}g")
            with col2:
                st.metric("Carbs Goal", f"{current_plan['carb_goal']}g")
                st.metric("Fat Goal", f"{current_plan['fat_goal']}g")
            
            st.metric("Fiber Goal", f"{current_plan['fiber_goal']}g")
            
            # Date range
            st.write(f"**Plan Period:** {current_plan['start_date']} to {current_plan['end_date']}")
            
            # Fetch meals for the current plan
            current_plan_id = current_plan['plan_id']
            meals_url = f"{MEALS_URL}/{current_plan_id}"
            meals_data = fetch_data(meals_url)
            
            if meals_data and len(meals_data) > 0:
                meals_df = pd.DataFrame(meals_data)
                
                # Display meals table
                st.subheader("Meals in Your Plan")
                
                # Customize the table
                meals_display = meals_df[['name', 'type', 'recipe', 'calories']].copy()
                st.dataframe(meals_display, use_container_width=True)
                
                # Create nutritional breakdown chart
                st.subheader("Nutritional Breakdown by Meal")
                
                # Prepare data for visualization
                chart_data = meals_df[['name', 'protein_intake', 'carb_intake', 'fat_intake', 'fiber_intake']].copy()
                
                # Melt the dataframe for better visualization
                melted_data = pd.melt(
                    chart_data, 
                    id_vars=['name'], 
                    value_vars=['protein_intake', 'carb_intake', 'fat_intake', 'fiber_intake'],
                    var_name='Nutrient', 
                    value_name='Grams'
                )
                
                # Clean up the nutrient names for display
                melted_data['Nutrient'] = melted_data['Nutrient'].str.replace('_intake', '')
                
                # Create the chart
                fig = px.bar(
                    melted_data, 
                    x='name', 
                    y='Grams', 
                    color='Nutrient',
                    barmode='group',
                    labels={'name': 'Meal', 'Grams': 'Grams (g)'},
                    title='Nutrient Breakdown by Meal'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Add a calorie distribution pie chart
                st.subheader("Calorie Distribution by Meal")
                pie_fig = px.pie(
                    meals_df, 
                    values='calories', 
                    names='name',
                    title='Calorie Distribution'
                )
                st.plotly_chart(pie_fig, use_container_width=True)
                
                # Display ingredients list
                st.subheader("Ingredients List")
                ingredients = meals_df['ingredients'].unique()
                
                # Create columns for better display
                cols = st.columns(3)
                for i, ingredient in enumerate(ingredients):
                    cols[i % 3].write(f"- {ingredient}")
            else:
                st.info("No meals found for your current plan. Please check with your nutritionist.")
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