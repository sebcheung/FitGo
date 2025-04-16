import logging
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Arnold\'s Diet Planner')
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}.")
else:
    st.write("### Welcome to your Diet Planner.")

MEAL_PLANS_URL = f"http://web-api:4000/n/meal-plans/31"

# Fetch meal plan data
def fetch_meal_plan():
    try:
        response = requests.get(MEAL_PLANS_URL, timeout=5)
        return response.json()[0] if response.status_code == 200 and response.json() else None
    except Exception as e:
        st.error(f"Error fetching meal plan: {str(e)}")
        return None

def get_sample_meals():
    return [
        {"Meal_ID": 373, "Plan_ID": 5, "Name": "Breakfast", "Type": "Normal", "Recipe": "Vegetable Stir Fry", 
         "Ingredients": "eggs", "Fiber_Intake": 14, "Carb_Intake": 91, "Calories": 1999, "Fat_Intake": 37, "Protein_Intake": 41},
        {"Meal_ID": 374, "Plan_ID": 5, "Name": "Lunch", "Type": "Normal", "Recipe": "Chicken Alfredo", 
         "Ingredients": "chicken, pasta", "Fiber_Intake": 22, "Carb_Intake": 65, "Calories": 750, "Fat_Intake": 25, "Protein_Intake": 45},
        {"Meal_ID": 375, "Plan_ID": 5, "Name": "Dinner", "Type": "Normal", "Recipe": "Salmon with Vegetables", 
         "Ingredients": "salmon, broccoli", "Fiber_Intake": 8, "Carb_Intake": 30, "Calories": 650, "Fat_Intake": 22, "Protein_Intake": 40},
        {"Meal_ID": 376, "Plan_ID": 5, "Name": "Snack", "Type": "Normal", "Recipe": "Greek Yogurt with Berries", 
         "Ingredients": "yogurt, berries", "Fiber_Intake": 3, "Carb_Intake": 20, "Calories": 180, "Fat_Intake": 3, "Protein_Intake": 15}
    ]

try:
    # Get meal plan data from API
    meal_plan = fetch_meal_plan()
    
    if meal_plan:
        # Display plan metrics
        st.subheader("Your Active Meal Plan")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Daily Calories", f"{meal_plan.get('Calories', 'N/A')} kcal")
            st.metric("Protein Goal", f"{meal_plan.get('Protein_Goal', 'N/A')}g")
        with col2:
            st.metric("Carbs Goal", f"{meal_plan.get('Carb_Goal', 'N/A')}g")
            st.metric("Fat Goal", f"{meal_plan.get('Fat_Goal', 'N/A')}g")
        
        st.metric("Fiber Goal", f"{meal_plan.get('Fiber_Goal', 'N/A')}g")
        
        # Format and display dates
        start_date = pd.to_datetime(meal_plan.get('Start_Date', 'N/A')).strftime('%Y-%m-%d') if meal_plan.get('Start_Date') else 'N/A'
        end_date = pd.to_datetime(meal_plan.get('End_Date', 'N/A')).strftime('%Y-%m-%d') if meal_plan.get('End_Date') else 'N/A'
        st.write(f"**Plan Period:** {start_date} to {end_date}")
        
        # Get sample meals
        meals_data = get_sample_meals()
        
        # Display meals table
        st.subheader("Your Meals")
        meals_df = pd.DataFrame(meals_data)
        st.dataframe(meals_df[['Name', 'Recipe', 'Ingredients', 'Calories', 'Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake']], 
                    use_container_width=True)
        
        # Create nutritional breakdown chart
        st.subheader("Nutritional Breakdown by Meal")
        
        # Prepare data for chart
        chart_data = meals_df[['Name', 'Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake']]
        melted_data = pd.melt(
            chart_data, 
            id_vars=['Name'], 
            value_vars=['Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake'],
            var_name='Nutrient', 
            value_name='Grams'
        )
        melted_data['Nutrient'] = melted_data['Nutrient'].str.replace('_Intake', '')
        
        # Create chart
        fig = px.bar(
            melted_data, 
            x='Name', 
            y='Grams', 
            color='Nutrient',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add calorie distribution pie chart
        st.subheader("Calorie Distribution")
        pie_fig = px.pie(meals_df, values='Calories', names='Name')
        st.plotly_chart(pie_fig, use_container_width=True)
        
        # Display ingredients list
        st.subheader("Ingredients List")
        ingredients = meals_df['Ingredients'].tolist()
        cols = st.columns(3)
        for i, ingredient in enumerate(ingredients):
            cols[i % 3].write(f"- {ingredient}")
    
    else:
        st.info("No meal plan found for this client.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")