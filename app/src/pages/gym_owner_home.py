import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Gym Owner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Manage Employee Roster', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_Manage_Emp.py')

if st.button('Manage Client Roster', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Diet_Planner.py')

if st.button('Create or Cancel Events', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Leaderboard.py')

if st.button('View Event Participant Lists', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Stats.py')

if st.button('Equipment Manager', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Stats.py')

