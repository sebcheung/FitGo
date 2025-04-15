import logging
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from modules.nav import SideBarLinks

# Set up page
SideBarLinks()
st.header('Arnold\'s Diet Planner')
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}.")
else:
    st.write("### Welcome to your Diet Planner.")

# API endpoints
MEAL_PLANS_URL = f"http://web-api:4000/n/meal-plans/31"
MEALS_URL = "http://web-api:4000/n/meals"

# Fetch data function
def fetch_data(url):
    try:
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Main app
try:
    with st.spinner("Loading..."):
        # Get meal plan data
        meal_plans_data = fetch_data(MEAL_PLANS_URL)
        
        if meal_plans_data and len(meal_plans_data) > 0:
            # Get current plan
            plan = meal_plans_data[0]
            
            # Display plan metrics
            st.subheader("Your Active Meal Plan")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Daily Calories", f"{plan.get('Calories', 'N/A')} kcal")
                st.metric("Protein Goal", f"{plan.get('Protein_Goal', 'N/A')}g")
            with col2:
                st.metric("Carbs Goal", f"{plan.get('Carb_Goal', 'N/A')}g")
                st.metric("Fat Goal", f"{plan.get('Fat_Goal', 'N/A')}g")
            
            st.metric("Fiber Goal", f"{plan.get('Fiber_Goal', 'N/A')}g")
            
            # Format and display dates
            start_date = pd.to_datetime(plan.get('Start_Date', 'N/A')).strftime('%Y-%m-%d') if plan.get('Start_Date') else 'N/A'
            end_date = pd.to_datetime(plan.get('End_Date', 'N/A')).strftime('%Y-%m-%d') if plan.get('End_Date') else 'N/A'
            st.write(f"**Plan Period:** {start_date} to {end_date}")
            
            # Get meals for this plan
            plan_id = plan.get('Plan_ID')
            if plan_id:
                meals_data = fetch_data(f"{MEALS_URL}/{plan_id}")
                
                if meals_data and len(meals_data) > 0:
                    # Display meals table
                    st.subheader("Your Meals")
                    meals_df = pd.DataFrame(meals_data)
                    st.dataframe(meals_df, use_container_width=True)
                    
                    # Create nutritional breakdown chart
                    if all(col in meals_df.columns for col in ['Name', 'Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake']):
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
                        if 'Calories' in meals_df.columns:
                            st.subheader("Calorie Distribution")
                            pie_fig = px.pie(meals_df, values='Calories', names='Name')
                            st.plotly_chart(pie_fig, use_container_width=True)
                else:
                    st.info("No meals found for your current plan.")
        else:
            st.info("No meal plans found.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")