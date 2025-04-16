import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Welcome to FitGo")

st.markdown("""
## Your All-in-One Fitness and Wellness Companion

FitGo is a comprehensive fitness and wellness platform designed to streamline your health journey by integrating multiple aspects of wellness tracking into a single, intuitive interface. Unlike other applications that focus on isolated aspects of health, FitGo brings together workout planning, nutrition tracking, personal coaching, and community engagement in one place.

### Why FitGo?

In today's fragmented fitness app landscape, users often juggle multiple platforms - one for tracking workouts, another for logging meals, and yet another for connecting with trainers. FitGo eliminates this complexity by providing a unified dashboard where all your health data comes together to create a complete picture of your wellness journey.

### Who Benefits from FitGo?

- **Fitness Enthusiasts** - Monitor performance metrics, track progress, and optimize workouts
- **Personal Trainers** - Manage client programs, track progress, and provide personalized guidance
- **Nutritionists** - Create and adjust meal plans based on real-time client data
- **Gym Owners** - Monitor facility usage, track member engagement, and optimize operations

### Key Features

- **Personalized Workout Tracking** - Log exercises, sets, reps, and weights with progress visualization
- **Nutrition Management** - Track meals, calories, and macronutrients with customized meal planning
- **Health Metrics Dashboard** - Monitor vital statistics like heart rate, sleep quality, and body composition
- **Leaderboards** - Stay motivated with friendly competition and community challenges
- **Professional Integration** - Connect with trainers and nutritionists for personalized guidance

### The FitGo Difference

What makes FitGo truly unique is how it leverages data integration to provide insights that would be impossible with separate apps. By analyzing the relationships between your nutrition, exercise, sleep, and other health metrics, FitGo helps you understand how different aspects of your lifestyle impact your overall wellbeing.

### Our Vision

We believe that health and fitness should be accessible and manageable for everyone. By simplifying the tracking process and providing actionable insights, FitGo aims to empower users to make informed decisions about their health and wellness journey.

Join us in revolutionizing how people approach fitness and wellness tracking!
""")

# Add a section about the technical implementation
st.subheader("About This Implementation")
st.markdown("""
This demo version of FitGo is built using:

- **Frontend**: Streamlit for interactive web interface with Plotly for data visualization
- **Backend**: Flask API for handling data requests and business logic
- **Database**: MySQL for secure and efficient data storage
- **Containerization**: Docker for consistent deployment across environments

The application follows a microservices architecture, with separate containers for the frontend, backend API, and database. This ensures scalability and maintainability as the platform grows.
""")

# Add a section for the team if desired
st.subheader("Project Team")
st.markdown("""
FitGo was developed as part of the CS 3200 Course Project by a team of dedicated students passionate about health technology and software development: Sebastian Cheung, Saachi Bhatia, Tarun Anbarasu, Naisha Mistry, and Andrei Zubek.
""")

# Add some spacing
st.write("")

# Add a call to action 
st.info("Explore the sidebar menu to discover all that FitGo has to offer!")