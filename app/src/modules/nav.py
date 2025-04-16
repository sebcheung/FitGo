# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ For Role of Client -------------------------------------------
def ClientsHomeNav():
    st.sidebar.page_link(
        "pages/00_Client_Home.py", label="Client Home", icon="🏋️"
    )

def WorkoutLog():
    st.sidebar.page_link(
        "pages/01_Workout_Log.py", label="Workout Log", icon="💪"
    )

def DietPlanner():
    st.sidebar.page_link(
        "pages/02_Diet_Planner.py", label="Diet Planner", icon="🍽️"
    )

def Leaderboard():
    st.sidebar.page_link(
        "pages/03_Leaderboard.py", label="Leaderboard", icon="🏆"
    )

def Stats():
    st.sidebar.page_link(
        "pages/04_Stats.py", label="Statistics and Health Metrics", icon="📊"
    )

#### ------------------------ For Role of Trainer -------------------------------------------
def TrainerHomeNav():
    st.sidebar.page_link(
        "pages/31_trainer_home.py", label="Trainer Home", icon="👟"
    )

def TrainerWorkoutPlans():
    st.sidebar.page_link(
        "pages/32_trainer_workout_plans.py", label="Workout Plans", icon="🔋"
    )

def TrainerCalendar():
    st.sidebar.page_link(
        "pages/33_trainer_calendar.py", label="Calendar", icon="📅"
    )

def Messages():
    st.sidebar.page_link(
        "pages/34_trainer_messages.py", label="Messages", icon="💬"
    )

def Resources():
    st.sidebar.page_link(
        "pages/34_trainer_resources.py", label="Resources", icon="🗃️"
    )

#### ------------------------ For Role of Nutritionist --------------------------------------
def NutritionistHomeNav():
    st.sidebar.page_link(
        "pages/40_nutritionist_home.py", label="Nutritionist Home", icon="🍃"
    )

def Restrictions():
    st.sidebar.page_link(
        "pages/41_nutritionist_restrictions.py", label="Restrictions", icon="❌"
    )

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/Fitgo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        # If the user is Client, show Workout Log, Leaderboard, Diet Planner, and Health Metrics
        if st.session_state["role"] == "client":
            ClientsHomeNav()
            WorkoutLog()
            DietPlanner()
            Leaderboard()
            Stats()
        
        # If the user is Trainer, show Workout Plans, Calendar, Messages, and Resources
        if st.session_state["role"] == "trainer":
            TrainerHomeNav()
            TrainerCalendar()
            Messages()
            TrainerWorkoutPlans()
            Resources()

        # If the user is Nutritionist, show Restrictions
        if st.session_state["role"] == "nutritionist":
            NutritionistHomeNav()
            Restrictions()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
