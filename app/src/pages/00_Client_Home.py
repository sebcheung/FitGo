import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Client, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Workout Log', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Workout_Log.py')

if st.button('View Diet Planner', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Diet_Planner.py')

if st.button('View Leaderboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Leaderboard.py')

if st.button('View Statistics and Health Metrics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Stats.py')
