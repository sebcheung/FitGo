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
  st.switch_page('pages/21_Manage_Emp.py')

if st.button('Manage Client Roster', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Manage_Clients.py')

if st.button('Manage Events', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Manage_Events.py')

if st.button('Manage Equipment', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Manage_Equip.py')

