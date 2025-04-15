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
            
            # Format dates for better display - handle potential column name variations
            date_columns = ['start_date', 'startdate', 'startDate', 'Start_date', 'Start_Date']
            for col in date_columns:
                if col in meal_plans_df.columns:
                    meal_plans_df[col] = pd.to_datetime(meal_plans_df[col]).dt.strftime('%Y-%m-%d')
                    break
                    
            end_date_columns = ['end_date', 'enddate', 'endDate', 'End_date', 'End_Date']
            for col in end_date_columns:
                if col in meal_plans_df.columns:
                    meal_plans_df[col] = pd.to_datetime(meal_plans_df[col]).dt.strftime('%Y-%m-%d')
                    break
            
            # Get the most recent meal plan
            current_plan = meal_plans_df.iloc[0]
            
            # Function to safely get a value from the plan using multiple potential column names
            def get_plan_value(column_variants, default="N/A"):
                for col in column_variants:
                    if col in current_plan:
                        return current_plan[col]
                return default
            
            # Display meal plan details in a nice format
            col1, col2 = st.columns(2)
            with col1:
                calories = get_plan_value(['calories', 'Calories', 'calorie', 'Calorie'])
                protein = get_plan_value(['protein_goal', 'proteinGoal', 'ProteinGoal', 'protein'])
                st.metric("Daily Calories", f"{calories} kcal")
                st.metric("Protein Goal", f"{protein}g")
            with col2:
                carbs = get_plan_value(['carb_goal', 'carbGoal', 'CarbGoal', 'carbs'])
                fat = get_plan_value(['fat_goal', 'fatGoal', 'FatGoal', 'fat'])
                st.metric("Carbs Goal", f"{carbs}g")
                st.metric("Fat Goal", f"{fat}g")
            
            fiber = get_plan_value(['fiber_goal', 'fiberGoal', 'FiberGoal', 'fiber'])
            st.metric("Fiber Goal", f"{fiber}g")
            
            # Date range
            start_date = get_plan_value(['start_date', 'startDate', 'StartDate', 'startdate'])
            end_date = get_plan_value(['end_date', 'endDate', 'EndDate', 'enddate'])
            st.write(f"**Plan Period:** {start_date} to {end_date}")
            
            # Fetch meals for the current plan
            plan_id = get_plan_value(['plan_id', 'planId', 'PlanId', 'id', 'ID'])
            meals_url = f"{MEALS_URL}/{plan_id}"
            meals_data = fetch_data(meals_url)
            
            if meals_data and len(meals_data) > 0:
                meals_df = pd.DataFrame(meals_data)
                
                # Display meals table
                st.subheader("Meals in Your Plan")
                
                # Identify available columns for displaying
                available_columns = []
                for col in ['name', 'type', 'recipe', 'calories']:
                    if col in meals_df.columns:
                        available_columns.append(col)
                
                if available_columns:
                    meals_display = meals_df[available_columns].copy()
                    st.dataframe(meals_display, use_container_width=True)
                else:
                    # If standard columns not found, show all columns
                    st.dataframe(meals_df, use_container_width=True)
                
                # Function to check if required columns exist for visualization
                def has_required_columns(df, required_cols):
                    return all(col in df.columns for col in required_cols)
                
                # Create nutritional breakdown chart if possible
                nutrient_cols = ['name', 'protein_intake', 'carb_intake', 'fat_intake', 'fiber_intake']
                if has_required_columns(meals_df, nutrient_cols):
                    st.subheader("Nutritional Breakdown by Meal")
                    
                    # Prepare data for visualization
                    chart_data = meals_df[nutrient_cols].copy()
                    
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
                    
                    # Add a calorie distribution pie chart if calories exist
                    if 'calories' in meals_df.columns:
                        st.subheader("Calorie Distribution by Meal")
                        pie_fig = px.pie(
                            meals_df, 
                            values='calories', 
                            names='name',
                            title='Calorie Distribution'
                        )
                        st.plotly_chart(pie_fig, use_container_width=True)
                
                # Display ingredients list if column exists
                if 'ingredients' in meals_df.columns:
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

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    logger.exception("Unexpected exception in diet planner app")
    
    # Add detailed error information
    with st.expander("Debug Information"):
        st.write(f"Error details: {str(e)}")
        import traceback
        st.code(traceback.format_exc())