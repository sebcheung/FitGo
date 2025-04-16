import logging
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from modules.nav import SideBarLinks

SideBarLinks()
st.header('Arnold\'s Diet Planner')

client_id = st.session_state.get('client_id', 31) 
if 'first_name' in st.session_state:
    st.write(f"### Hi, {st.session_state['first_name']}.")
else:
    st.write("### Welcome to your Diet Planner.")
MEAL_PLANS_URL = f"http://web-api:4000/n/meal-plans/{client_id}"
MEALS_URL = f"http://web-api:4000/n/meals"

# Fetch meal plan data
def fetch_meal_plan():
    try:
        response = requests.get(MEAL_PLANS_URL, timeout=5)
        return response.json()[0] if response.status_code == 200 and response.json() else None
    except Exception as e:
        st.error(f"Error fetching meal plan: {str(e)}")
        return None

# Fetch meals from API
def fetch_meals():
    try:
        response = requests.get(MEALS_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching meals: {str(e)}")
        return []

# Add a new meal
def post_meal(meal_data):
    try:
        response = requests.post(MEALS_URL, json=meal_data)
        if response.status_code == 201:
            st.success("Meal added successfully.")
        else:
            st.error(f"Failed to add meal: {response.text}")
    except Exception as e:
        st.error(f"Error adding meal: {str(e)}")

# Update a meal
def put_meal(meal_data):
    try:
        response = requests.put(MEALS_URL, json=meal_data)
        if response.status_code == 200:
            st.success("Meal updated successfully.")
        else:
            st.error(f"Failed to update meal: {response.text}")
    except Exception as e:
        st.error(f"Error updating meal: {str(e)}")

# Delete a meal
def delete_meal(meal_id):
    try:
        response = requests.delete(MEALS_URL, params={"meal_id": meal_id})
        if response.status_code == 200:
            st.success("Meal deleted successfully.")
        else:
            st.error(f"Failed to delete meal: {response.text}")
    except Exception as e:
        st.error(f"Error deleting meal: {str(e)}")

# Main logic
try:
    meal_plan = fetch_meal_plan()
    meals_data = fetch_meals()

    if meal_plan:
        st.subheader("Your Active Meal Plan")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Daily Calories", f"{meal_plan.get('Calories', 'N/A')} kcal")
            st.metric("Protein Goal", f"{meal_plan.get('Protein_Goal', 'N/A')}g")
        with col2:
            st.metric("Carbs Goal", f"{meal_plan.get('Carb_Goal', 'N/A')}g")
            st.metric("Fat Goal", f"{meal_plan.get('Fat_Goal', 'N/A')}g")

        st.metric("Fiber Goal", f"{meal_plan.get('Fiber_Goal', 'N/A')}g")

        start_date = pd.to_datetime(meal_plan.get('Start_Date', 'N/A')).strftime('%Y-%m-%d') if meal_plan.get('Start_Date') else 'N/A'
        end_date = pd.to_datetime(meal_plan.get('End_Date', 'N/A')).strftime('%Y-%m-%d') if meal_plan.get('End_Date') else 'N/A'
        st.write(f"**Plan Period:** {start_date} to {end_date}")

        if meals_data:
            meals_df = pd.DataFrame(meals_data)
            st.subheader("Your Meals")
            st.dataframe(meals_df[['Name', 'Recipe', 'Ingredients', 'Calories', 'Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake']],
                         use_container_width=True)

            st.subheader("Nutritional Breakdown by Meal")
            chart_data = meals_df[['Name', 'Protein_Intake', 'Carb_Intake', 'Fat_Intake', 'Fiber_Intake']]
            melted_data = pd.melt(chart_data, id_vars=['Name'], var_name='Nutrient', value_name='Grams')
            melted_data['Nutrient'] = melted_data['Nutrient'].str.replace('_Intake', '')
            fig = px.bar(melted_data, x='Name', y='Grams', color='Nutrient', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Calorie Distribution")
            pie_fig = px.pie(meals_df, values='Calories', names='Name')
            st.plotly_chart(pie_fig, use_container_width=True)

            st.subheader("Ingredients List")
            ingredients = meals_df['Ingredients'].dropna().tolist()
            cols = st.columns(3)
            for i, ingredient in enumerate(ingredients):
                cols[i % 3].write(f"- {ingredient}")

            # Update or delete meals
            selected_meal = st.selectbox("Select a meal to update or delete", meals_df['Name'].tolist())
            meal_row = meals_df[meals_df['Name'] == selected_meal].iloc[0]

            with st.expander("Update Meal"):
                with st.form("update_meal"):
                    new_name = st.text_input("Name", value=meal_row['Name'])
                    new_type = st.text_input("Type", value=meal_row['Type'])
                    new_recipe = st.text_area("Recipe", value=meal_row['Recipe'])
                    new_ingredients = st.text_area("Ingredients", value=meal_row['Ingredients'])
                    submit = st.form_submit_button("Update")
                    if submit:
                        put_meal({
                            "Meal_ID": int(meal_row['Meal_ID']),
                            "Name": new_name,
                            "Type": new_type,
                            "Recipe": new_recipe,
                            "Ingredients": new_ingredients
                        })

            with st.expander("Delete Meal"):
                if st.button("Delete"):
                    delete_meal(meal_row['Meal_ID'])

        # Add new meal
        st.subheader("Add New Meal")
        with st.form("add_meal"):
            name = st.text_input("Meal Name")
            type_ = st.text_input("Type")
            recipe = st.text_area("Recipe")
            ingredients = st.text_area("Ingredients")
            plan_id = meal_plan['Plan_ID']
            submit = st.form_submit_button("Add")
            if submit:
                post_meal({
                    "Plan_ID": plan_id,
                    "Name": name,
                    "Type": type_,
                    "Recipe": recipe,
                    "Ingredients": ingredients
                })

    else:
        st.info("No meal plan found for this client.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")